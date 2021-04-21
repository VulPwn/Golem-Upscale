FROM tensorflow/tensorflow:1.2.0-gpu
RUN set -xe 		\
    && echo '#!/bin/sh' > /usr/sbin/policy-rc.d 	\
    && echo 'exit 101' >> /usr/sbin/policy-rc.d 	\
    && chmod +x /usr/sbin/policy-rc.d 		\
    && dpkg-divert --local --rename --add /sbin/initctl 	\
    && cp -a /usr/sbin/policy-rc.d /sbin/initctl 	\
    && sed -i 's/^exit.*/exit 0/' /sbin/initctl 		\
    && echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup 		\
    && echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean 	\
    && echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean 	\
    && echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean 		\
    && echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages 		\
    && echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes 		\
    && echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests
RUN rm -rf /var/lib/apt/lists/*
RUN sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list
RUN mkdir -p /run/systemd \
    && echo 'docker' > /run/systemd/container
CMD ["/bin/bash"]
LABEL maintainer=NVIDIA_CORPORATION_<cudatools@nvidia.com>
LABEL com.nvidia.volumes.needed=nvidia_driver
RUN NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 \
    &&     NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 \
    &&     apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub \
    &&     apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub \
    &&     echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - \
    && rm cudasign.pub \
    &&     echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list
ENV CUDA_VERSION=8.0.61
LABEL com.nvidia.cuda.version=8.0.61
ENV CUDA_PKG_VERSION=8-0=8.0.61-1
RUN apt-get update \
    && apt-get install -y --no-install-recommends         cuda-nvrtc-$CUDA_PKG_VERSION         cuda-nvgraph-$CUDA_PKG_VERSION         cuda-cusolver-$CUDA_PKG_VERSION         cuda-cublas-8-0=8.0.61.1-1         cuda-cufft-$CUDA_PKG_VERSION         cuda-curand-$CUDA_PKG_VERSION         cuda-cusparse-$CUDA_PKG_VERSION         cuda-npp-$CUDA_PKG_VERSION         cuda-cudart-$CUDA_PKG_VERSION \
    &&     ln -s cuda-8.0 /usr/local/cuda \
    &&     rm -rf /var/lib/apt/lists/*
RUN echo "/usr/local/cuda/lib64" >> /etc/ld.so.conf.d/cuda.conf \
    &&     ldconfig
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \
    &&     echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf
ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64
LABEL com.nvidia.build.id=17805093 com.nvidia.build.ref=9673f05290f77b37078cf3e0ccc9bab583a8a552
LABEL maintainer=NVIDIA_CORPORATION_<cudatools@nvidia.com>
RUN apt-get update \
    && apt-get install -y --no-install-recommends         cuda-core-$CUDA_PKG_VERSION         cuda-misc-headers-$CUDA_PKG_VERSION         cuda-command-line-tools-$CUDA_PKG_VERSION         cuda-nvrtc-dev-$CUDA_PKG_VERSION         cuda-nvml-dev-$CUDA_PKG_VERSION         cuda-nvgraph-dev-$CUDA_PKG_VERSION         cuda-cusolver-dev-$CUDA_PKG_VERSION         cuda-cublas-dev-8-0=8.0.61.1-1         cuda-cufft-dev-$CUDA_PKG_VERSION         cuda-curand-dev-$CUDA_PKG_VERSION         cuda-cusparse-dev-$CUDA_PKG_VERSION         cuda-npp-dev-$CUDA_PKG_VERSION         cuda-cudart-dev-$CUDA_PKG_VERSION         cuda-driver-dev-$CUDA_PKG_VERSION \
    &&     rm -rf /var/lib/apt/lists/*
ENV LIBRARY_PATH=/usr/local/cuda/lib64/stubs:
LABEL maintainer=NVIDIA_CORPORATION_<cudatools@nvidia.com>
RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list
ENV CUDNN_VERSION=5.1.10
LABEL com.nvidia.cudnn.version=5.1.10
RUN apt-get update \
    && apt-get install -y --no-install-recommends             libcudnn5=$CUDNN_VERSION-1+cuda8.0             libcudnn5-dev=$CUDNN_VERSION-1+cuda8.0 \
    &&     rm -rf /var/lib/apt/lists/*
MAINTAINER VulPwn <manorris403@gmail.com>
RUN apt-get update \
    && apt-get install -y --no-install-recommends         build-essential         curl         libfreetype6-dev         libpng12-dev         libzmq3-dev         pkg-config         python         python-dev         rsync         software-properties-common         unzip         \
    &&     apt-get clean \
    &&     rm -rf /var/lib/apt/lists/*
RUN curl -O https://bootstrap.pypa.io/pip/2.7/get-pip.py \
    &&     python get-pip.py \
    &&     rm get-pip.py
RUN pip --no-cache-dir install        matplotlib         numpy         scipy         sklearn         pandas         Pillow
RUN pip --no-cache-dir install http://ci.tensorflow.org/view/Release/job/release-matrix-linux-gpu/TF_BUILD_CONTAINER_TYPE=GPU,TF_BUILD_IS_OPT=OPT,TF_BUILD_IS_PIP=PIP,TF_BUILD_PYTHON_VERSION=PYTHON2,label=gpu-linux/lastSuccessfulBuild/artifact/pip_test/whl/tensorflow_gpu-1.2.0-cp27-cp27mu-manylinux1_x86_64.whl
ENV LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
ADD SRGAN-tensorflow /SRGAN-tensorflow
VOLUME /SRGAN-tensorflow/data /SRGAN-tensorflow/result
WORKDIR /SRGAN-tensorflow
