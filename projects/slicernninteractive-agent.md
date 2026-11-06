We have added **nnInteractive Agent** to [SlicerNNInteractive](https://github.com/coendevente/SlicerNNInteractive), bringing segmentation through plain-language requests into 3D Slicer. The integration builds on nnInteractive Agent by Fabian Isensee and colleagues. You describe what you want segmented, and an AI agent locates the structures, places prompts for nnInteractive, inspects the results, and refines them in response to your feedback.

The agent takes over the sequence of interactions that a human would otherwise perform manually. For example, a request such as “segment every rib individually” gives it a task to work through using the image and the segmentation tools. Claude Code and Codex are supported, alongside configurable model servers. The underlying segmentation still comes from nnInteractive; the agent decides how to use it to carry out the request.

### Demo video

<video controls preload="metadata" playsinline style="width:100%;height:auto;" aria-label="SlicerNNInteractive demonstration"><source src="https://github.com/user-attachments/assets/8a6a7fc7-df8d-47d9-b13d-1d6a49df16a7" type="video/mp4">Your browser does not support embedded video. <a href="https://github.com/user-attachments/assets/8a6a7fc7-df8d-47d9-b13d-1d6a49df16a7">Watch the demonstration on GitHub</a>.</video>

The conversation and the images inspected by the agent appear in the module, while completed objects are added to a Slicer segmentation. You can review the result in the familiar slice and 3D views, ask for changes, or send an existing segmentation to the agent for further work.

The agent can use image renderings and associated information when communicating with its configured model provider. Choose a provider or locally hosted model appropriate for your data. Installation and configuration details are in the [SlicerNNInteractive README](https://github.com/coendevente/SlicerNNInteractive#nninteractive-agent-segment-from-a-text-request).
