#!/usr/bin/env python3
import asyncio
from datetime import timedelta
import pathlib
import sys
import os

from yapapi import (
    Executor,
    Task,
    __version__ as yapapi_version,
    WorkContext,
    windows_event_loop_fix,
)
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.package import vm
from yapapi.rest.activity import BatchTimeoutError

# For importing `utils.py`:
script_dir = pathlib.Path(__file__).resolve().parent
parent_directory = script_dir.parent
sys.stderr.write(f"Adding {parent_directory} to sys.path.\n")
sys.path.append(str(parent_directory))
import utils  # noqa

os.environ["YAGNA_APPKEY"] = "9bcc8f2f74974ffeaf7fc16161b0ccc1"

img = ""
image_dir = script_dir / "data"
images = image_dir.glob('*.png')
for i in images:
    img = i.name

async def main(subnet_tag: str):
    package = await vm.repo(
        image_hash="04b96edbd8510bdec37ed24b8efd9ce4800e079716ec7afba3800e95",
        min_mem_gib=2.0,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        scene_path = str(script_dir / "data" / img)
        ctx.send_file(scene_path, "/SRGAN-tensorflow/data/" + img)
        async for task in tasks:
            ctx.run("/SRGAN-tensorflow/main.py")
            output_file = script_dir / "result" / img
            ctx.download_file("/SRGAN-tensorflow/result/images/" + img, output_file)
            try:
                # Set timeout for executing the script on the provider. Two minutes is plenty
                # of time for computing a single frame, for other tasks it may be not enough.
                # If the timeout is exceeded, this worker instance will be shut down and all
                # remaining tasks, including the current one, will be computed by other providers.
                yield ctx.commit(timeout=timedelta(seconds=1800))
                # TODO: Check if job results are valid
                # and reject by: task.reject_task(reason = 'invalid file')
                task.accept_result(result=output_file)
            except BatchTimeoutError:
                print(
                    f"{utils.TEXT_COLOR_RED}"
                    f"Task timed out: {task}, time: {task.running_time}"
                    f"{utils.TEXT_COLOR_DEFAULT}"
                )
                raise

    # Iterator over the frame indices that we want to render
    frames: range = range(0, 1)
    # Worst-case overhead, in minutes, for initialization (negotiation, file transfer etc.)
    # TODO: make this dynamic, e.g. depending on the size of files to transfer
    init_overhead = 3
    # Providers will not accept work if the timeout is outside of the [5 min, 30min] range.
    # We increase the lower bound to 6 min to account for the time needed for our demand to
    # reach the providers.
    min_timeout, max_timeout = 6, 30

    timeout = timedelta(minutes=max(
        min(init_overhead + len(frames) * 2, max_timeout), min_timeout))

    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Executor(
        package=package,
        max_workers=3,
        budget=10.0,
        timeout=timeout,
        subnet_tag=subnet_tag,
        event_consumer=log_summary(log_event_repr),
    ) as executor:

        async for task in executor.submit(worker, [Task(data=frame) for frame in frames]):
            print(
                f"{utils.TEXT_COLOR_CYAN}"
                f"Task computed: {task}, result: {task.result}, time: {task.running_time}"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )


if __name__ == "__main__":
    parser = utils.build_parser("Render blender scene")
    parser.set_defaults(log_file="blender-yapapi.log")
    args = parser.parse_args()

    # This is only required when running on Windows with Python prior to 3.8:
    windows_event_loop_fix()

    enable_default_logger(log_file=args.log_file)

    loop = asyncio.get_event_loop()

    subnet = args.subnet_tag
    sys.stderr.write(
        f"yapapi version: {utils.TEXT_COLOR_YELLOW}{yapapi_version}{utils.TEXT_COLOR_DEFAULT}\n"
    )
    sys.stderr.write(
        f"Using subnet: {utils.TEXT_COLOR_YELLOW}{subnet}{utils.TEXT_COLOR_DEFAULT}\n")
    task = loop.create_task(main(subnet_tag=args.subnet_tag))
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print(
            f"{utils.TEXT_COLOR_YELLOW}"
            "Shutting down gracefully, please wait a short while "
            "or press Ctrl+C to exit immediately..."
            f"{utils.TEXT_COLOR_DEFAULT}"
        )
        task.cancel()
        try:
            loop.run_until_complete(task)
            print(
                f"{utils.TEXT_COLOR_YELLOW}"
                "Shutdown completed, thank you for waiting!"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass
