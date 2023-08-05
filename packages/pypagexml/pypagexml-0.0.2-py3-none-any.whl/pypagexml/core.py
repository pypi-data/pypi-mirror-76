from typing import Optional
from PIL import Image

import pypagexml.ds as ds


def new_document(metadata: Optional[ds.MetadataType], page: Optional[ds.PageType] = None) -> ds.PcGtsTypeSub:
    doc = ds.PcGtsTypeSub(
        Metadata=metadata if metadata is not None else ds.MetadataTypeSub.default(),
        Page=page)
    return doc


def new_document_from_image(path: str, metadata: Optional[ds.MetadataType] = None) -> ds.PcGtsTypeSub:
    im = Image.open(path)
    w = im.width
    h = im.height
    xres, yres = im.info['dpi'] if 'dpi' in im.info else (None, None)

    return ds.PcGtsTypeSub(
        Metadata=metadata if metadata is not None else ds.MetadataTypeSub.default(),
        Page=ds.PageTypeSub(
            imageFilename=path, imageWidth=w, imageHeight=h, imageXResolution=xres, imageYResolution=yres
        )
    )


import re

RE_POSTFIX_NUM = re.compile("^.*[^0-9]([0-9]+)$")


def maxid(regions):
    def idnum(s):
        m = RE_POSTFIX_NUM.match(s.get_id)
        return m.groups() if m is not None else ()

    return max([int(k)
                for x in regions
                for k in idnum(x)
                ])


class PageXml:

    def __init__(self, pcgts: ds.PcGtsTypeSub):
        self.pcgts = pcgts
        self.text_maxid = maxid(pcgts.get_Page().get_TextRegion())
        self.img_maxid = maxid(pcgts.get_Page().get_ImageRegion())

    def next_text_id(self):
        id = f"rtxt{self.text_maxid}"
        self.text_maxid += 1
        return id

    def next_image_id(self):
        id = f"rimg{self.img_maxid}"
        self.img_maxid += 1
        return id

    def add_paragraph(self, p, coords: ds.Points, ptype="paragraph"):
        page = self.pcgts.get_Page()
        page.add_TextRegion(
            ds.TextRegionTypeSub(
                id=self.next_text_id(), Coords=ds.CoordsTypeSub.with_points(coords), type_=ptype
            )
        )

    def add_image(self, p, coords: ds.Points):
        page = self.pcgts.get_Page()
        page.add_ImageRegion(
            ds.ImageRegionTypeSub(
                id=self.next_text_id(), Coords=ds.CoordsTypeSub.with_points(coords)
            )
        )
