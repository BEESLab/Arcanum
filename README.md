# Arcanum

This is the repository for our paper "Arcanum: Detecting and Evaluating the Privacy Risks of Browser Extensions on Web Pages and Web Content" published" in USENIX Security Symposium 2024.

At the moment, we have uploaded the source code of Arcanum, our tainted tracking system built upon Chromium version 108 (git tag: 108.0.5359.71, git commit: bc8aa10cc7044a60ece07cd8ec1730870071da04). Before apply the patches to Chromium's source code, make sure to build an unmodified Chromium locally first. You can follow the [official instruction](https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md). We have also set up a Docker image (docker pull xqgtiti/arcanum_build:v1) that has the necessary environment for building Arcanum.

**Note that we are in the process of submitting our source code to the Artifact Evaluation of USENIX's Winter Cycle Deadline (June 13, 2024) for the Artifacts Available, Artifacts Functional, and Results Reproduced badges. We will provide more detailed instructions (as an artifact appendix in the paper) in June, including instructions for building Chromium 108, applying patches, comments for the source code, and sample extensions for testing, etc. If you would like use our code before then and have any questions, please feel free to contact Qinge Xie: qxie47@gatech.edu.**
