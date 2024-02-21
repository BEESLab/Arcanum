### 1. Build An Unmodified Chromium from Source Code

Arcanum is built upon on Chromium version 108.0.5359.71, before apply the patches, make sure to build an unmodified Chromium locally first. You can also follow the [official instruction](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md)

#### 1. Install depot_tools

* Clone the `depot_tools` repository: `git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git`
* Add `depot_tools` to your `PATH` such as `export PATH="/path/to/depot_tools:$PATH"`

#### 2. Get Chromium code

* Create a `chromium` directory for the checkout and change to it, such as:`mkdir ~/chromium && cd ~/chromium`
* Run the `fetch` tool from depot_tools to check out the code and its dependencies: `fetch --nohooks chromium`. The command is expected to take 30 minutes on even a fast connection, and many hours on slower ones. (it takes ~)

#### 3. Switch to the 108 branch

Next, switch to the version 108 branch, you can also follow the [offical instruction](https://www.chromium.org/developers/how-tos/get-the-code/working-with-release-branches/). This part should only need to be done once, but it won't hurt to repeat it

* Make sure you are in 'src': 


