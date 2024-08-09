## Overview
This repository holds the artifacts of our paper ["Arcanum: Detecting and Evaluating the Privacy Risks of Browser Extensions on Web Pages and Web Content"](https://www.usenix.org/conference/usenixsecurity24/presentation/xie-qinge) in USENIX Security Symposium 2024. In this work, we develop Arcanum, a dynamic taint tracking system for modern Chrome extensions designed to monitor the flow of sensitive user content from web pages. A key feature of Arcanum is allowing researchers to instrument specific web page elements as tainted at runtime via JS DOM annotations. More information about Arcanum can be found in our paper. This artifact includes: 
- `patches/`: The Arcanum prototype is built on Chromium Browser version 108.0.5359.71. We provide all Chromium patches of the Arcanum implementation. 
- `Sample_Extensions/`: We provide two types of sample extensions in this artifact as the dataset.  
	- **Custom Extensions**: Sample extensions implemented by ourselves to demonstrate how extensions can be tested using Arcanum, on seven websites that were experimented with in our paper (Amazon, Facebook, Gmail, Instagram, LinkedIn, Outlook, and PayPal). For each site, we provide one Manifest Version 2 (MV2) extension and one Manifest Version 3 (MV3) extension. Besides, we also provide other custom extensions to guide users in testing the taint tracking process of Arcanum, including testing different taint sources, sinks, and propagation cases.
	- **Real-world Extensions**: Representative extensions from the Chrome Web Store that have been tested and flagged by Arcanum. Specifically, we include all extensions discussed in the case studies of Section 4.10, as well as those listed in Table 7 of Section 4.5 (i.e., the flagged extensions with the most users in each web content category) in our paper. 
- `annotations/`:  JavaScript files for annotating specific DOM elements on each target web page. 
- `recordings/`: Recordings for each target web page.
- `Test_Cases/`: Python test case scripts for each sample extension. 
- `Taint_Logs/`: Taint logs (i.e., analysis results generated by Arcanum) for each real-world extension obtained from the experiments conducted in our paper.
- `WprGo_Ad_Nonce`: The modified WprGo script for replaying the Gmail test page. It has been included in the Docker image we provide and will be automatically used in our test cases when testing the Gmail case.

## Dependencies
**Hardware**: A x86_64 (amd64) machine with at least 8 GiB RAM, 4 cores/8 threads CPU, and at least 100 GiB of free disk space is required. More than 16 GiB RAM is highly recommended. For reference, our experiments were conducted on a physical machine with 512 GiB RAM, 32 cores/128 threads CPU, running Ubuntu 20.04.6 LTS (Kernel Linux 5.4.0-173-generic). The provided test cases have also been tested on another Linux server with 8 CPU cores and 16 GiB RAM. If you are using a machine with fewer CPU resources, you might need to adjust the values of `--custom-script-idle-timeout-ms` and `--custom-delay-for-animation-ms` switches in the Python code for Facebook and Gmail test cases, as the CPU resources will impact the page load time when replaying (see explanations in Section 3.4 in our paper). 

**Software**: 
- To build Arcanum, we provide a [Docker image](https://hub.docker.com/r/xqgtiti/arcanum_build) (Ubuntu 20.04) that includes all necessary dependencies for building a version of Chromium patched with the Arcanum implementation. Alternatively, users can follow the [official instruction](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#Docker) to build your own Docker container.
- To run Arcanum, we provide a [Docker image](https://hub.docker.com/r/xqgtiti/arcanum_run) (Ubuntu 18.04) that includes all necessary dependencies. We strongly recommend using this pre-configured image, as our test case scripts partly rely on its settings (such as software executable paths). If you choose to build the environment manually, the following software dependencies are required: [Go 1.19.12 Linux](https://go.dev/dl/go1.19.12.linux-amd64.tar.gz), [WprGo v0.0.0-20230901234838-f16ca3c78e46](https://chromium.googlesource.com/catapult/+/HEAD/web_page_replay_go/), Python 3.8.0 Linux (with Selenium 4, pyvirtualdisplay), [ChromeDriver 108.0.5359.71](https://developer.chrome.com/docs/chromedriver/downloads#chromedriver_1080535971), Xvfb, and [Chromium Dependencies](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md#Install-additional-build-dependencies).
While we have not verified compatibility with versions other than those listed above, we believe that our artifacts will work with Ubuntu 18.04, 20.04, and 22.04, Python 3.8+ (Selenium 4), and any versions of Xvfb and WprGo.

## Build
Here we describe how to set up a build environment for Chromium and build a version of Chromium with the patches of the Arcanum implementation. The set-up is mostly based on the [official Chromium build instructions](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md) on Linux.
1. Clone the Chromium depot tools to a specific directory (e.g., `$HOME`) on the host machine and add their path to the `PATH` environment variable.
    ```
    $ git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    $ export PATH="${HOME}/depot_tools:$PATH"
    ```
2. Get the Chromium source code (this may take a while depending on your network connection)
    ```
    $ mkdir ${HOME}/chromium && cd ${HOME}/chromium/
    $ fetch --nohooks chromium
    ```
3. In `src/`, check out the branch for Chromium version 108.0.5359.71. You could also refer to the [official instructions](https://www.chromium.org/developers/how-tos/get-the-code/working-with-release-branches/) on working with Chromium release branches. 
    ```
    $ cd src
    $ gclient sync --with_branch_heads --with_tags
    $ git fetch
    $ git checkout tags/108.0.5359.71
    $ gclient sync --with_branch_heads --with_tags
    ```
3. Prepare the Docker container for building. Pull the provided Docker image for building, then launch a Docker container from this image. Make sure to mount the host directory containing the Chromium source code and depot_tools into the container:
     ```
     $ docker pull xqgtiti/arcanum_build:latest
     $ docker run -it --mount src=${HOME},target="/mnt/build/",type=bind --name=build xqgtiti/arcanum_build:latest
     ```
 4. Prepare build in the Docker container’s interactive shell. Add the path of Chromium depot tools to the `PATH` environment variable. The command `gn args ...` automatically opens a file (`args.gn`) in the default text editor. Replace the contents of this file with the contents of the file `build/args.gn` from in this repository.
     ```
     $ export PATH="/mnt/build/depot_tools:$PATH"
     $ cd /mnt/build/chromium/src/
     $ gn args out/Default
     ```
5. After updating the contents of the `args.gn` file, run the above command again to finalize the build preparations: `gn args out/Default`.
6. Build an unmodified Chrome and its Linux installer (this may take a while depending on the host machine’s performance). 
    ```
    $ ninja -C out/Default chrome
    $ ninja -C out/Default "chrome/installer/linux:unstable_deb"
    ```
7. Build a version of Chrome patched with the Arcanum implementation.
    ```
    $ cd /mnt/build/chromium/src/
    $ git apply ~/patches/chromium.patch
    $ cd /mnt/build/chromium/src/v8/
    $ git apply ~/patches/v8.patch
    $
    $ cd /mnt/build/chromium/src/
    $ gn args out/Arcanum
    $ cp out/Default/gn.args out/Arcanum/
    $ gn args out/Arcanum
    $ ninja -C out/Arcanum chrome
    ```
8. Build a Linux installer for Arcanum, you can then find the .deb file in `out/Arcanum/`.
    ```
    $ ninja -C out/Arcanum "chrome/installer/linux:unstable_deb"
    $ cd /mnt/build/chromium/src/out/Arcanum/
    $ ls chromium-browser-unstable_108.0.5359.71-1_amd64.deb
    ```
    
## Basic Test

Pull the provided Docker image for running Arcanum, and then launch a Docker container from this image. Note that the `--privileged` flag is required. You can also mount any directory that is convenient for transferring files from the host machine.
```
$ docker pull xqgtiti/arcanum_run:latest
$ docker run -it --privileged --name=run xqgtiti/arcanum_run:latest
```
Copy the Arcanum installer file (i.e., the .deb file) to `/root/Arcanum/` in the Docker container and decompress it. Note that we use this path in the test case code as the Arcanum executable path. Please modify the variable in the code if you place the installer elsewhere.
```
$ cd /root/Arcanum/
$ ar x chromium-browser-unstable_108.0.5359.71-1_amd64.deb
$ tar -xvf data.tar && tar -xvf control.tar
```
Run the basic test case in the interactive shell of the container, using the pre-configured Python 3.8: `python3.8 ~/Test_Cases/Basic_Test.py`. The basic test case uses Selenium to launch Arcanum (a modified Chromium) with a pre-installed empty extension and navigates to a web page. If Arcanum runs normally, you should see `Basic Test: Success.` in the output.

## Test Custom Extensions (~1 human-hour)
**Preparation**: Use the same Docker container from the Basic Test that has the Arcanum executable file in `/root/Arcanum/`. Download all custom extensions (in `Sample_Extensions/Custom/`) and copy the extensions to `/root/extensions/custom/` in the container.
```
$ mkdir -p /root/extensions/custom/
$ cp -r ~/Sample_Extensions/Custom/* /root/extensions/custom/
```
Download all recordings and JS scripts for DOM element annotations from the artifact Git repository and put them in the `/root/` directory in the container:
```
$ mkdir -p /root/recordings/
$ cp -r ~/recordings/* /root/recordings/
$ mkdir -p /root/annotations/
$ cp -r ~/annotations/* /root/annotations/
```
**Execution**: We have prepared a test case for each custom extension. Run these test cases in the container shell using the pre-configured Python 3.8: `python3.8 ~/Test_Cases/Custom_Test.py`
Each test case launches Arcanum with the corresponding web recording and DOM element annotations (or without annotations when testing non-web-content taint sources), and checks whether we successfully obtain the expected content in the taint logs, demonstrating the correct taint tracking of Arcanum. You can test all custom extensions together or test a specific extension by simply commenting out other test cases in `Custom_Test.py`. 

**Results**: For each extension being tested, you should see `Custom Extension ${Name}: Success.` in the test case output, demonstrating the correct taint tracking of Arcanum. You can refer to the test case code to see the expected content in the taint logs for each extension.

## Test Real-world Extensions (~1 human-hour)
**Preparation**: Use the same Docker container from the Basic Test that has the Arcanum executable filein `/root/Arcanum/`. Download all real-world extensions (in `∼/Sample_Extensions/Realworld/`) from the artifact Git repository and copy the extensions to `/root/extensions/realworld/` in the container.
```
$ mkdir -p /root/extensions/realworld/
$ cp -r ~/Sample_Extensions/Realworld/* /root/extensions/realworld/
```
**Execution**: We have prepared a test case for each realworld extension. Run these test cases in the container shell using the pre-configured Python 3.8: `python3.8 ~/Test_Cases/Realworld_Test.py`. 
Each test case launches Arcanum with the corresponding web recording and DOM element annotations, and checks whether we successfully obtain the expected content in the taint logs, aligning with the experiment results described in Sections 4.5 and 4.10. You can test all real-world extensions together or test a specific extension by simply commenting out other test cases in `Realworld_Test.py`.

**Results**: For each extension being tested, you should see `Real-world Extension ${ID}: Success.` in the test case output. You can refer to the test case code to see the expected content in the taint logs for each extension. We also release all taint logs (i.e., analysis results generated by Arcanum) for each real-world extension obtained from the experiments conducted in our paper. Please check these logs located in `Taint_Logs/`. 

## Other Notes
* Arcanum’s taint source logs, propagation logs, and the storage sink logs are located in `/ram/analysis/v8logs/`. All other taint sink logs are in the user data directory of Chromium.
* When testing Arcanum with Docker, ensure to allocate sufficient CPU resources (4 logical processors or more), especially when running multiple containers in parallel (e.g., using `--cpus=4 --cpuset-cpus=0-3`). Use `--cpuset-cpus` to specify CPUs in scenarios where preemption may occur.
* As described in Section 3.4 in the paper, we introduce a forced delay in Arcanum to ensure that a target web page will fully load before an extension injects its content script. We configure this delay as a Chrome switch `--custom-script-idle-timeout-ms` and `--custom-delay-for-animation-ms`. Users can set a specific delay when recording and replaying different web pages according to their page loading times. Please refer to the provided test cases for examples of its usage. The test cases were evaluated on a Linux server with 8 CPUs and 16 GiB of RAM. If you are testing with fewer CPU resources, please consider increasing the value of the two switches mentioned above in the test case scripts.

## Citation
If you use our system in your research, please cite our work using this Bibtex entry:
```
@inproceedings{xiearcanum_usenix24,
  title = {Arcanum: Detecting and Evaluating the Privacy Risks of Browser Extensions on Web Pages and Web Content},
  author={Xie, Qinge and Murali, Manoj Vignesh Kasi and Pearce, Paul and Li, Frank}
  year = {2024},
  booktitle={USENIX Security Symposium (USENIX Security 24)},
}
```
