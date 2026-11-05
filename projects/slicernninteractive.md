[SlicerNNInteractive](https://github.com/coendevente/SlicerNNInteractive) brings interactive, AI-assisted segmentation of 3D medical images into 3D Slicer. It connects Slicer's image viewing and annotation tools with **nnInteractive**, the promptable segmentation framework developed by Fabian Isensee and colleagues. You indicate a structure, inspect the proposed segmentation, and refine it with further prompts. This makes it easier to create detailed annotations without outlining every slice by hand.

The plugin supports **points, scribbles, bounding boxes, and lassos**. These interactions let you identify the target and correct areas that need attention while working directly with the volume. The result is a 3D segmentation that you can inspect in Slicer's slice views and 3D viewer. Keyboard shortcuts help keep the annotation process moving when working through multiple structures.

### Watch the interactive workflow

The demonstration below shows the prompting workflow in Slicer. Each interaction gives the model more information about the intended structure, so you can build up a segmentation and correct its boundaries as you go.

<video controls preload="metadata" playsinline style="width:100%;height:auto;" aria-label="SlicerNNInteractive demonstration"><source src="https://github.com/user-attachments/assets/c9f9ee0a-f74d-4907-aa21-484dcfd10948" type="video/mp4">Your browser does not support embedded video. <a href="https://github.com/user-attachments/assets/c9f9ee0a-f74d-4907-aa21-484dcfd10948">Watch the demonstration on GitHub</a>.</video>

The extension separates the annotation interface from model inference through a client-server architecture. This allows you to use Slicer on your workstation while running the model on a GPU server, or run both on the same machine. See the [repository](https://github.com/coendevente/SlicerNNInteractive) for installation instructions and the current feature set.

*Publication update: the JOSS paper below was published in July 2026, after the original date of this post.*
