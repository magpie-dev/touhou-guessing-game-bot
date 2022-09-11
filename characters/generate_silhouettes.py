import asyncio
import pathlib

import numpy as np
from PIL import Image

from characters.utils import get_id


async def create_silhouette(filepath: pathlib.Path) -> None:
    loop = asyncio.get_running_loop()

    image = await loop.run_in_executor(None, Image.open, filepath.absolute())

    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r.fill(0)
    g.fill(0)
    b.fill(0)
    x = np.dstack([r, g, b, a])

    image = Image.fromarray(x, "RGBA")

    file = filepath.with_stem(str(get_id(filepath.stem))).name
    filepath = filepath.parent.parent / "silhouettes" / file

    await loop.run_in_executor(None, image.save, filepath.absolute())


async def async_main() -> None:
    path = pathlib.Path("resources/images")
    await asyncio.gather(
        *(create_silhouette(filepath) for filepath in path.glob("*.png"))
    )


def main() -> None:
    asyncio.new_event_loop().run_until_complete(async_main())
