# MCP server integrating with ComfyUI for image generation
# to run: python server.py stdio workingdirectory
# NB expects workflows to be a subfolder in workingdirectory

import sys
import os
import pathlib
import logging
from mcp.server.fastmcp import FastMCP
from comfyui_client import ComfyUIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MCP_Server")

comfyui_client = ComfyUIClient("http://localhost:8188")
mcp = FastMCP("ComfyUI_MCP_Server")


# define the image generation tool
@mcp.tool()
def generate_image(prompt: str, workflow_id="basic_api_test", width=None, height=None, model=None) -> dict:
    """Generate an image using ComfyUI"""
    logger.info(
        f"Received request with params: prompt={prompt}, workflow_id={workflow_id}, "
        f"width={width}, height={height}, model={model}"
    )
    try:
        # Use global comfyui_client (since mcp.context isn’t available)
        image_url = comfyui_client.generate_image(
            prompt=prompt,
            width=width,
            height=height,
            workflow_id=workflow_id,
            model=model
        )
        logger.info(f"Returning image URL: {image_url}")
        return {"image_url": image_url}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}


# define a resource to list available workflow ids
@mcp.resource("workflows://available")
def list_workflows() -> list:
    """List available workflows in ComfyUI"""
    workflows = comfyui_client.get_available_workflows()
    logger.info(f"Available workflow ids: {workflows}")
    return workflows


if __name__ == "__main__":
    # search for a working directory argument and change directory to it
    for arg in sys.argv:
        p = pathlib.Path(arg)
        if p.is_absolute() and p.exists() and p.is_dir():
            os.chdir(p)
            logger.info(f"Changed working directory to: {p}")
            break
    mcp.run()
