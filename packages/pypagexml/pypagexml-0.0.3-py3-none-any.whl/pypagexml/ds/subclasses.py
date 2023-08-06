#!/usr/bin/env python

#
# Generated Fri Jun 26 10:29:12 2020 by generateDS.py version 2.35.24.
# Python 3.7.7 (default, May 20 2020, 14:10:14)  [GCC 9.3.0]
#
# Command line options:
#   ('-o', 'pypagexml/ds/generated.py')
#   ('-s', 'pypagexml/ds/subclasses.py')
#
# Command line arguments:
#   data/pagecontent.xsd
#
# Current working directory (os.getcwd()):
#   pagexml
#
from __future__ import annotations

import os
import sys
from typing import List, Tuple, Optional, Union

from .util import iso_now

from lxml import etree as etree_

import pypagexml.ds.generated as supermod


def parsexml_(infile: Union[os.PathLike, str], parser=None):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser)
    return doc


def parsexmlstring_(instring: str, parser=None):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser)
    return element


#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True


#
# Data representation classes
#


class PcGtsTypeSub(supermod.PcGtsType):
    def __init__(self, pcGtsId: str = None, Metadata: MetadataTypeSub = None, Page: PageTypeSub = None):
        super(PcGtsTypeSub, self).__init__(pcGtsId, Metadata, Page)

    def update_modification_time(self):
        self.Metadata.set_LastChange(iso_now())


supermod.PcGtsType.subclass = PcGtsTypeSub


# end class PcGtsTypeSub


class MetadataTypeSub(supermod.MetadataType):
    def __init__(self, Creator: str, Created: str,
                 LastChange: Optional[str] = None, externalRef: str = None, Comments: Optional[List[str]] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None,
                 MetadataItem: Optional[List[MetadataTypeSub]] = None):
        super(MetadataTypeSub, self).__init__(externalRef, Creator, Created, LastChange or Created, Comments, UserDefined,
                                              MetadataItem)

    @staticmethod
    def default() -> MetadataTypeSub:
        from pypagexml import PCGTS_CREATOR
        now = iso_now()
        return MetadataTypeSub(
            Creator=PCGTS_CREATOR,
            Created=now,
            LastChange=now,
        )


supermod.MetadataType.subclass = MetadataTypeSub


# end class MetadataTypeSub


class MetadataItemTypeSub(supermod.MetadataItemType):
    def __init__(self, type_: Optional[str] = None, name: Optional[str] = None, value: str = None,
                 date: Optional[str] = None,
                 Labels: Optional[List[LabelsTypeSub]] = None):
        super(MetadataItemTypeSub, self).__init__(type_, name, value, date, Labels)


supermod.MetadataItemType.subclass = MetadataItemTypeSub


# end class MetadataItemTypeSub


class LabelsTypeSub(supermod.LabelsType):
    def __init__(self, externalModel: Optional[str] = None, externalId: Optional[str] = None,
                 prefix: Optional[str] = None, comments: Optional[str] = None,
                 Label: Optional[List[LabelTypeSub]] = None):
        super(LabelsTypeSub, self).__init__(externalModel, externalId, prefix, comments, Label)


supermod.LabelsType.subclass = LabelsTypeSub


# end class LabelsTypeSub


class LabelTypeSub(supermod.LabelType):
    def __init__(self, value: str, type_: Optional[str] = None, comments: Optional[str] = None):
        super(LabelTypeSub, self).__init__(value, type_, comments)


supermod.LabelType.subclass = LabelTypeSub


# end class LabelTypeSub


class PageTypeSub(supermod.PageType):
    def __init__(self, imageFilename: str = None, imageWidth: int = None, imageHeight: int = None,
                 imageXResolution: float = None, imageYResolution: float = None, imageResolutionUnit: str = None,
                 custom: str = None, orientation: float = None, type_: str = None, primaryLanguage: str = None,
                 secondaryLanguage: str = None, primaryScript: str = None, secondaryScript: str = None,
                 readingDirection: str = None, textLineOrder: str = None, conf: float = None,
                 AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Border: Optional[BorderTypeSub] = None,
                 PrintSpace: Optional[PrintSpaceTypeSub] = None, ReadingOrder: Optional[ReadingOrderTypeSub] = None,
                 Layers: Optional[LayersTypeSub] = None, Relations: Optional[RelationsTypeSub] = None,
                 TextStyle: Optional[TextStyleTypeSub] = None, UserDefined: Optional[UserDefinedTypeSub] = None,
                 Labels: Optional[LabelsTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 MapRegion: Optional[List[MapRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None):
        super(PageTypeSub, self).__init__(imageFilename, imageWidth, imageHeight, imageXResolution, imageYResolution,
                                          imageResolutionUnit, custom, orientation, type_, primaryLanguage,
                                          secondaryLanguage, primaryScript, secondaryScript, readingDirection,
                                          textLineOrder, conf, AlternativeImage, Border, PrintSpace, ReadingOrder,
                                          Layers, Relations, TextStyle, UserDefined, Labels, TextRegion, ImageRegion,
                                          LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion, MapRegion,
                                          SeparatorRegion, MathsRegion, ChemRegion, MusicRegion, AdvertRegion,
                                          NoiseRegion, UnknownRegion, CustomRegion)


supermod.PageType.subclass = PageTypeSub

# end class PageTypeSub

Points = List[Tuple[int, int]]


class CoordsTypeSub(supermod.CoordsType):
    def __init__(self, points: Optional[str] = None, conf: Optional[float] = None):
        super(CoordsTypeSub, self).__init__(points, conf)

    @staticmethod
    def with_points(points: Points) -> CoordsTypeSub:
        return CoordsTypeSub(points=points_to_string(points))


supermod.CoordsType.subclass = CoordsTypeSub


def points_to_string(points: Points) -> str:
    return " ".join(",".join(map(str, p)) for p in points)


# end class CoordsTypeSub


class TextLineTypeSub(supermod.TextLineType):
    def __init__(self, id: str, primaryLanguage: Optional[str] = None, primaryScript: Optional[str] = None, secondaryScript: Optional[str] = None, readingDirection: Optional[str] = None,
                 production: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, index: Optional[int] = None,
                 AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 Baseline: Optional[BaselineTypeSub] = None, Word: Optional[List[WordTypeSub]] = None,
                 TextEquiv: Optional[List[TextEquivTypeSub]] = None, TextStyle: Optional[TextStyleTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None):
        super(TextLineTypeSub, self).__init__(id, primaryLanguage, primaryScript, secondaryScript, readingDirection,
                                              production, custom, comments, index, AlternativeImage, Coords, Baseline,
                                              Word, TextEquiv, TextStyle, UserDefined, Labels)


supermod.TextLineType.subclass = TextLineTypeSub


# end class TextLineTypeSub


class WordTypeSub(supermod.WordType):
    def __init__(self, id: str, language: Optional[str] = None, primaryScript: Optional[str] = None, secondaryScript: Optional[str] = None, readingDirection: Optional[str] = None,
                 production: Optional[str] = None, custom: Optional[str] = None, comments: Optional[str] = None,
                 AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None, Glyph: Optional[List[GlyphTypeSub]] = None,
                 TextEquiv: Optional[List[TextEquivTypeSub]] = None, TextStyle: Optional[TextStyleTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None):
        super(WordTypeSub, self).__init__(id, language, primaryScript, secondaryScript, readingDirection, production,
                                          custom, comments, AlternativeImage, Coords, Glyph, TextEquiv, TextStyle,
                                          UserDefined, Labels)


supermod.WordType.subclass = WordTypeSub


# end class WordTypeSub


class GlyphTypeSub(supermod.GlyphType):
    def __init__(self, id: str, ligature: Optional[bool] = None, symbol: Optional[bool] = None, script: Optional[str] = None, production: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None,
                 AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None, Graphemes:
            Optional[GraphemesTypeSub] = None,
                 TextEquiv: Optional[List[TextEquivTypeSub]] = None, TextStyle: Optional[TextStyleTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None,
                 Labels: Optional[List[LabelsTypeSub]] = None):
        super(GlyphTypeSub, self).__init__(id, ligature, symbol, script, production, custom, comments, AlternativeImage,
                                           Coords, Graphemes, TextEquiv, TextStyle, UserDefined, Labels)


supermod.GlyphType.subclass = GlyphTypeSub


# end class GlyphTypeSub


class TextEquivTypeSub(supermod.TextEquivType):
    def __init__(self, index: Optional[int] = None, conf: Optional[float] =
            None, dataType: Optional[str] = None, dataTypeDetails: Optional[str] = None, comments: Optional[str] = None,
                 PlainText: Optional[str] = None,
                 Unicode: Optional[str] = None):
        super(TextEquivTypeSub, self).__init__(index, conf, dataType, dataTypeDetails, comments, PlainText, Unicode)


supermod.TextEquivType.subclass = TextEquivTypeSub


# end class TextEquivTypeSub


class GridTypeSub(supermod.GridType):
    def __init__(self, GridPoints: Optional[List[GridPointsTypeSub]] = None):
        super(GridTypeSub, self).__init__(GridPoints)


supermod.GridType.subclass = GridTypeSub


# end class GridTypeSub


class GridPointsTypeSub(supermod.GridPointsType):
    def __init__(self, index: int = None, points: Optional[str] = None):
        super(GridPointsTypeSub, self).__init__(index, points)


supermod.GridPointsType.subclass = GridPointsTypeSub


# end class GridPointsTypeSub


class PrintSpaceTypeSub(supermod.PrintSpaceType):
    def __init__(self, Coords: Optional[CoordsTypeSub] = None):
        super(PrintSpaceTypeSub, self).__init__(Coords)


supermod.PrintSpaceType.subclass = PrintSpaceTypeSub


# end class PrintSpaceTypeSub


class ReadingOrderTypeSub(supermod.ReadingOrderType):
    def __init__(self, conf: Optional[float] = None, OrderedGroup: Optional[OrderedGroupTypeSub] = None,
                 UnorderedGroup: Optional[UnorderedGroupTypeSub] = None):
        super(ReadingOrderTypeSub, self).__init__(conf, OrderedGroup, UnorderedGroup)


supermod.ReadingOrderType.subclass = ReadingOrderTypeSub


# end class ReadingOrderTypeSub


class RegionRefIndexedTypeSub(supermod.RegionRefIndexedType):
    def __init__(self, index: int = None, regionRef: str = None):
        super(RegionRefIndexedTypeSub, self).__init__(index, regionRef)


supermod.RegionRefIndexedType.subclass = RegionRefIndexedTypeSub


# end class RegionRefIndexedTypeSub


class OrderedGroupIndexedTypeSub(supermod.OrderedGroupIndexedType):
    def __init__(self, id: str, regionRef: Optional[str] = None, index: int = None, caption: Optional[str] = None, type_: Optional[str] = None,
                 continuation: Optional[bool] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, UserDefined: Optional[UserDefinedTypeSub] = None,
                 Labels: Optional[List[LabelsTypeSub]] = None,
                 RegionRefIndexed: Optional[List[RegionRefIndexedTypeSub]] = None,
                 OrderedGroupIndexed: Optional[List[OrderedGroupIndexedTypeSub]] = None,
                 UnorderedGroupIndexed: Optional[List[UnorderedGroupIndexedTypeSub]] = None):
        super(OrderedGroupIndexedTypeSub, self).__init__(id, regionRef, index, caption, type_, continuation, custom,
                                                         comments, UserDefined, Labels, RegionRefIndexed,
                                                         OrderedGroupIndexed, UnorderedGroupIndexed)


supermod.OrderedGroupIndexedType.subclass = OrderedGroupIndexedTypeSub


# end class OrderedGroupIndexedTypeSub


class UnorderedGroupIndexedTypeSub(supermod.UnorderedGroupIndexedType):
    def __init__(self, id: str, regionRef: Optional[str] = None, index: int = None, caption: Optional[str] = None, type_: Optional[str] = None,
                 continuation: Optional[bool] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, UserDefined: Optional[UserDefinedTypeSub] = None,
                 Labels: Optional[List[LabelsTypeSub]] = None, RegionRef: Optional[List[RegionRefTypeSub]] = None,
                 OrderedGroup: Optional[OrderedGroupTypeSub] = None,
                 UnorderedGroup: Optional[UnorderedGroupTypeSub] = None):
        super(UnorderedGroupIndexedTypeSub, self).__init__(id, regionRef, index, caption, type_, continuation, custom,
                                                           comments, UserDefined, Labels, RegionRef, OrderedGroup,
                                                           UnorderedGroup)


supermod.UnorderedGroupIndexedType.subclass = UnorderedGroupIndexedTypeSub


# end class UnorderedGroupIndexedTypeSub


class RegionRefTypeSub(supermod.RegionRefType):
    def __init__(self, regionRef: str):
        super(RegionRefTypeSub, self).__init__(regionRef)


supermod.RegionRefType.subclass = RegionRefTypeSub


# end class RegionRefTypeSub


class OrderedGroupTypeSub(supermod.OrderedGroupType):
    def __init__(self, id: str, regionRef: Optional[str] = None, caption: Optional[str] = None, type_: Optional[str] = None, continuation: Optional[bool] = None,
                 custom: Optional[str] = None, comments: Optional[str] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 RegionRefIndexed: Optional[List[RegionRefIndexedTypeSub]] = None,
                 OrderedGroupIndexed: Optional[List[OrderedGroupIndexedTypeSub]] = None,
                 UnorderedGroupIndexed: Optional[List[UnorderedGroupIndexedTypeSub]] = None):
        super(OrderedGroupTypeSub, self).__init__(id, regionRef, caption, type_, continuation, custom, comments,
                                                  UserDefined, Labels, RegionRefIndexed, OrderedGroupIndexed,
                                                  UnorderedGroupIndexed)


supermod.OrderedGroupType.subclass = OrderedGroupTypeSub


# end class OrderedGroupTypeSub


class UnorderedGroupTypeSub(supermod.UnorderedGroupType):
    def __init__(self, id: str, regionRef: Optional[str] = None, caption: Optional[str] = None, type_: Optional[str] = None, continuation: Optional[bool] = None,
                 custom: Optional[str] = None, comments: Optional[str] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 RegionRef: Optional[List[RegionRefTypeSub]] = None, OrderedGroup: Optional[OrderedGroupTypeSub] = None,
                 UnorderedGroup: Optional[UnorderedGroupTypeSub] = None):
        super(UnorderedGroupTypeSub, self).__init__(id, regionRef, caption, type_, continuation, custom, comments,
                                                    UserDefined, Labels, RegionRef, OrderedGroup, UnorderedGroup)


supermod.UnorderedGroupType.subclass = UnorderedGroupTypeSub


# end class UnorderedGroupTypeSub


class BorderTypeSub(supermod.BorderType):
    def __init__(self, Coords: Optional[CoordsTypeSub] = None):
        super(BorderTypeSub, self).__init__(Coords)


supermod.BorderType.subclass = BorderTypeSub


# end class BorderTypeSub


class LayersTypeSub(supermod.LayersType):
    def __init__(self, Layer: Optional[LayerTypeSub] = None):
        super(LayersTypeSub, self).__init__(Layer)


supermod.LayersType.subclass = LayersTypeSub


# end class LayersTypeSub


class LayerTypeSub(supermod.LayerType):
    def __init__(self, id: str, zIndex: int, caption: Optional[str] = None, RegionRef: Optional[List[RegionRefTypeSub]] = None):
        super(LayerTypeSub, self).__init__(id, zIndex, caption, RegionRef)


supermod.LayerType.subclass = LayerTypeSub


# end class LayerTypeSub


class BaselineTypeSub(supermod.BaselineType):
    def __init__(self, points: Optional[str] = None, conf: Optional[float] = None):
        super(BaselineTypeSub, self).__init__(points, conf)


supermod.BaselineType.subclass = BaselineTypeSub


# end class BaselineTypeSub


class RelationsTypeSub(supermod.RelationsType):
    def __init__(self, Relation: Optional[List[RelationTypeSub]] = None):
        super(RelationsTypeSub, self).__init__(Relation)


supermod.RelationsType.subclass = RelationsTypeSub


# end class RelationsTypeSub


class RelationTypeSub(supermod.RelationType):
    def __init__(self, id: str, type_: Optional[str] = None, custom: Optional[str] = None, comments: Optional[str] = None,
                 Labels: Optional[List[LabelsTypeSub]] = None, SourceRegionRef: Optional[RegionRefTypeSub] = None,
                 TargetRegionRef: Optional[RegionRefTypeSub] = None):
        super(RelationTypeSub, self).__init__(id, type_, custom, comments, Labels, SourceRegionRef, TargetRegionRef)


supermod.RelationType.subclass = RelationTypeSub


# end class RelationTypeSub


class TextStyleTypeSub(supermod.TextStyleType):
    def __init__(self, fontFamily: Optional[str] = None, serif:
            Optional[bool] = None, monospace: Optional[bool] = None, fontSize:
            Optional[float] = None, xHeight: Optional[int] = None, kerning:
            Optional[int] = None,
            textColour: Optional[str] = None, textColourRgb: Optional[int] =
            None, bgColour: Optional[str] = None, bgColourRgb: Optional[int] =
            None, reverseVideo: Optional[bool] = None, bold: Optional[bool] = None,
            italic: Optional[bool] = None, underlined: Optional[bool] = None,
            underlineStyle: Optional[str] = None, subscript: Optional[bool] = None, superscript: Optional[bool] = None,
            strikethrough: Optional[bool] = None, smallCaps: Optional[bool] =
            None, letterSpaced: Optional[int] = None):
        super(TextStyleTypeSub, self).__init__(fontFamily, serif, monospace, fontSize, xHeight, kerning, textColour,
                                               textColourRgb, bgColour, bgColourRgb, reverseVideo, bold, italic,
                                               underlined, underlineStyle, subscript, superscript, strikethrough,
                                               smallCaps, letterSpaced)


supermod.TextStyleType.subclass = TextStyleTypeSub


# end class TextStyleTypeSub


class RegionTypeSub(supermod.RegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 extensiontype_=None):
        super(RegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords, UserDefined,
                                            Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion, GraphicRegion,
                                            TableRegion, ChartRegion, SeparatorRegion, MathsRegion, ChemRegion,
                                            MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion, CustomRegion,
                                            extensiontype_)


supermod.RegionType.subclass = RegionTypeSub


# end class RegionTypeSub


class AlternativeImageTypeSub(supermod.AlternativeImageType):
    def __init__(self, filename: str, comments: Optional[str] = None, conf: Optional[float] = None):
        super(AlternativeImageTypeSub, self).__init__(filename, comments, conf)


supermod.AlternativeImageType.subclass = AlternativeImageTypeSub


# end class AlternativeImageTypeSub


class GraphemesTypeSub(supermod.GraphemesType):
    def __init__(self, Grapheme: Optional[List[GraphemeTypeSub]] = None,
                 NonPrintingChar: Optional[List[NonPrintingCharTypeSub]] = None,
                 GraphemeGroup: Optional[List[GraphemeGroupTypeSub]] = None):
        super(GraphemesTypeSub, self).__init__(Grapheme, NonPrintingChar, GraphemeGroup)


supermod.GraphemesType.subclass = GraphemesTypeSub


# end class GraphemesTypeSub


class GraphemeBaseTypeSub(supermod.GraphemeBaseType):
    def __init__(self, id: str, index: int = None, ligature: Optional[bool] = None, charType: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, TextEquiv: Optional[List[TextEquivTypeSub]] = None,
                 extensiontype_=None):
        super(GraphemeBaseTypeSub, self).__init__(id, index, ligature, charType, custom, comments, TextEquiv,
                                                  extensiontype_)


supermod.GraphemeBaseType.subclass = GraphemeBaseTypeSub


# end class GraphemeBaseTypeSub


class GraphemeTypeSub(supermod.GraphemeType):
    def __init__(self, id: str, index: int = None, ligature: Optional[bool] = None, charType: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, TextEquiv: Optional[List[TextEquivTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None):
        super(GraphemeTypeSub, self).__init__(id, index, ligature, charType, custom, comments, TextEquiv, Coords)


supermod.GraphemeType.subclass = GraphemeTypeSub


# end class GraphemeTypeSub


class NonPrintingCharTypeSub(supermod.NonPrintingCharType):
    def __init__(self, id: str, index: int = None, ligature: Optional[bool] = None, charType: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, TextEquiv: Optional[List[TextEquivTypeSub]] = None):
        super(NonPrintingCharTypeSub, self).__init__(id, index, ligature, charType, custom, comments, TextEquiv)


supermod.NonPrintingCharType.subclass = NonPrintingCharTypeSub


# end class NonPrintingCharTypeSub


class GraphemeGroupTypeSub(supermod.GraphemeGroupType):
    def __init__(self, id: str, index: int = None, ligature: Optional[bool] = None, charType: Optional[str] = None, custom: Optional[str] = None,
                 comments: Optional[str] = None, TextEquiv: Optional[List[TextEquivTypeSub]] = None,
                 Grapheme: Optional[List[GraphemeTypeSub]] = None,
                 NonPrintingChar: Optional[List[NonPrintingCharTypeSub]] = None):
        super(GraphemeGroupTypeSub, self).__init__(id, index, ligature, charType, custom, comments, TextEquiv, Grapheme,
                                                   NonPrintingChar)


supermod.GraphemeGroupType.subclass = GraphemeGroupTypeSub


# end class GraphemeGroupTypeSub


class UserDefinedTypeSub(supermod.UserDefinedType):
    def __init__(self, UserAttribute: Optional[List[UserAttributeTypeSub]] = None):
        super(UserDefinedTypeSub, self).__init__(UserAttribute)


supermod.UserDefinedType.subclass = UserDefinedTypeSub


# end class UserDefinedTypeSub


class UserAttributeTypeSub(supermod.UserAttributeType):
    def __init__(self, name: Optional[str] = None, description: Optional[str] =
            None, type_: Optional[str] = None, value: Optional[str] = None):
        super(UserAttributeTypeSub, self).__init__(name, description, type_, value)


supermod.UserAttributeType.subclass = UserAttributeTypeSub


# end class UserAttributeTypeSub


class TableCellRoleTypeSub(supermod.TableCellRoleType):
    def __init__(self, rowIndex: int = None, columnIndex: int = None, rowSpan:
            Optional[int] = None, colSpan: Optional[int] = None, header:
            Optional[bool] = None):
        super(TableCellRoleTypeSub, self).__init__(rowIndex, columnIndex, rowSpan, colSpan, header)


supermod.TableCellRoleType.subclass = TableCellRoleTypeSub


# end class TableCellRoleTypeSub


class RolesTypeSub(supermod.RolesType):
    def __init__(self, TableCellRole: Optional[TableCellRoleTypeSub] = None):
        super(RolesTypeSub, self).__init__(TableCellRole)


supermod.RolesType.subclass = RolesTypeSub


# end class RolesTypeSub


class CustomRegionTypeSub(supermod.CustomRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 type_: Optional[str] = None):
        super(CustomRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                  UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                  LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                  SeparatorRegion, MathsRegion, ChemRegion, MusicRegion, AdvertRegion,
                                                  NoiseRegion, UnknownRegion, CustomRegion, type_)


supermod.CustomRegionType.subclass = CustomRegionTypeSub


# end class CustomRegionTypeSub


class UnknownRegionTypeSub(supermod.UnknownRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None):
        super(UnknownRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                   UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                   LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                   SeparatorRegion, MathsRegion, ChemRegion, MusicRegion, AdvertRegion,
                                                   NoiseRegion, UnknownRegion, CustomRegion)


supermod.UnknownRegionType.subclass = UnknownRegionTypeSub


# end class UnknownRegionTypeSub


class NoiseRegionTypeSub(supermod.NoiseRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None):
        super(NoiseRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion)


supermod.NoiseRegionType.subclass = NoiseRegionTypeSub


# end class NoiseRegionTypeSub


class AdvertRegionTypeSub(supermod.AdvertRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, bgColour: Optional[str] = None):
        super(AdvertRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                  UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                  LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                  SeparatorRegion, MathsRegion, ChemRegion, MusicRegion, AdvertRegion,
                                                  NoiseRegion, UnknownRegion, CustomRegion, orientation, bgColour)


supermod.AdvertRegionType.subclass = AdvertRegionTypeSub


# end class AdvertRegionTypeSub


class MusicRegionTypeSub(supermod.MusicRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, bgColour: Optional[str] = None):
        super(MusicRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion, orientation, bgColour)


supermod.MusicRegionType.subclass = MusicRegionTypeSub


# end class MusicRegionTypeSub


class MapRegionTypeSub(supermod.MapRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None):
        super(MapRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                               UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                               GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                               ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                               CustomRegion, orientation)


supermod.MapRegionType.subclass = MapRegionTypeSub


# end class MapRegionTypeSub


class ChemRegionTypeSub(supermod.ChemRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, bgColour: Optional[str] = None):
        super(ChemRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                CustomRegion, orientation, bgColour)


supermod.ChemRegionType.subclass = ChemRegionTypeSub


# end class ChemRegionTypeSub


class MathsRegionTypeSub(supermod.MathsRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, bgColour: Optional[str] = None):
        super(MathsRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion, orientation, bgColour)


supermod.MathsRegionType.subclass = MathsRegionTypeSub


# end class MathsRegionTypeSub


class SeparatorRegionTypeSub(supermod.SeparatorRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, colour: Optional[str] = None):
        super(SeparatorRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                     UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                     LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                     SeparatorRegion, MathsRegion, ChemRegion, MusicRegion,
                                                     AdvertRegion, NoiseRegion, UnknownRegion, CustomRegion,
                                                     orientation, colour)


supermod.SeparatorRegionType.subclass = SeparatorRegionTypeSub


# end class SeparatorRegionTypeSub


class ChartRegionTypeSub(supermod.ChartRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, type_: Optional[str] =
                 None, numColours: Optional[int] = None, bgColour: Optional[str]
                 = None, embText: Optional[bool] = None):
        super(ChartRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion, orientation, type_, numColours, bgColour, embText)


supermod.ChartRegionType.subclass = ChartRegionTypeSub


# end class ChartRegionTypeSub


class TableRegionTypeSub(supermod.TableRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, rows: Optional[int] = None, columns: Optional[int] = None, lineColour: Optional[str] = None, bgColour: Optional[str] = None,
                 lineSeparators: Optional[bool] = None, embText: Optional[bool] = None, Grid: Optional[str] = None):
        super(TableRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion, orientation, rows, columns, lineColour, bgColour,
                                                 lineSeparators, embText, Grid)


supermod.TableRegionType.subclass = TableRegionTypeSub


# end class TableRegionTypeSub


class GraphicRegionTypeSub(supermod.GraphicRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, type_: Optional[str] =
                 None, numColours: Optional[int] = None, embText: Optional[bool]
                 = None):
        super(GraphicRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                   UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                   LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                   SeparatorRegion, MathsRegion, ChemRegion, MusicRegion, AdvertRegion,
                                                   NoiseRegion, UnknownRegion, CustomRegion, orientation, type_,
                                                   numColours, embText)


supermod.GraphicRegionType.subclass = GraphicRegionTypeSub


# end class GraphicRegionTypeSub


class LineDrawingRegionTypeSub(supermod.LineDrawingRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, penColour: Optional[str] = None, bgColour: Optional[str] = None, embText: Optional[bool] = None):
        super(LineDrawingRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                       UserDefined, Labels, Roles, TextRegion, ImageRegion,
                                                       LineDrawingRegion, GraphicRegion, TableRegion, ChartRegion,
                                                       SeparatorRegion, MathsRegion, ChemRegion, MusicRegion,
                                                       AdvertRegion, NoiseRegion, UnknownRegion, CustomRegion,
                                                       orientation, penColour, bgColour, embText)


supermod.LineDrawingRegionType.subclass = LineDrawingRegionTypeSub


# end class LineDrawingRegionTypeSub


class ImageRegionTypeSub(supermod.ImageRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, colourDepth: Optional[str] = None, bgColour: Optional[str] = None, embText: Optional[bool] = None):
        super(ImageRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                 UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                 GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                 ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                 CustomRegion, orientation, colourDepth, bgColour, embText)


supermod.ImageRegionType.subclass = ImageRegionTypeSub


# end class ImageRegionTypeSub


class TextRegionTypeSub(supermod.TextRegionType):
    def __init__(self, id: str, custom: Optional[str] = None, comments: Optional[str] = None,
                 continuation: Optional[bool] = None, AlternativeImage: Optional[List[AlternativeImageTypeSub]] = None,
                 Coords: Optional[CoordsTypeSub] = None,
                 UserDefined: Optional[UserDefinedTypeSub] = None, Labels: Optional[List[LabelsTypeSub]] = None,
                 Roles: Optional[RolesTypeSub] = None,
                 TextRegion: Optional[List[TextRegionTypeSub]] = None,
                 ImageRegion: Optional[List[ImageRegionTypeSub]] = None,
                 LineDrawingRegion: Optional[List[LineDrawingRegionTypeSub]] = None,
                 GraphicRegion: Optional[List[GraphicRegionTypeSub]] = None,
                 TableRegion: Optional[List[TableRegionTypeSub]] = None,
                 ChartRegion: Optional[List[ChartRegionTypeSub]] = None,
                 SeparatorRegion: Optional[List[SeparatorRegionTypeSub]] = None,
                 MathsRegion: Optional[List[MathsRegionTypeSub]] = None,
                 ChemRegion: Optional[List[ChemRegionTypeSub]] = None,
                 MusicRegion: Optional[List[MusicRegionTypeSub]] = None,
                 AdvertRegion: Optional[List[AdvertRegionTypeSub]] = None,
                 NoiseRegion: Optional[List[NoiseRegionTypeSub]] = None,
                 UnknownRegion: Optional[List[UnknownRegionTypeSub]] = None,
                 CustomRegion: Optional[List[CustomRegionTypeSub]] = None,
                 orientation: Optional[float] = None, type_: Optional[str] = None,
                 leading: Optional[int] = None, readingDirection: Optional[str] = None,
                 textLineOrder: Optional[str] = None, readingOrientation:
                 Optional[float] = None, indented: Optional[bool] = None, align: Optional[str] = None, primaryLanguage: Optional[str] = None,
                 secondaryLanguage: Optional[str] = None, primaryScript: Optional[str] = None,
                 secondaryScript: Optional[str] = None, production: Optional[str] = None, TextLine: Optional[List[TextLineTypeSub]] = None,
                 TextEquiv: Optional[List[TextEquivTypeSub]] = None, TextStyle: Optional[TextStyleTypeSub] = None):
        super(TextRegionTypeSub, self).__init__(id, custom, comments, continuation, AlternativeImage, Coords,
                                                UserDefined, Labels, Roles, TextRegion, ImageRegion, LineDrawingRegion,
                                                GraphicRegion, TableRegion, ChartRegion, SeparatorRegion, MathsRegion,
                                                ChemRegion, MusicRegion, AdvertRegion, NoiseRegion, UnknownRegion,
                                                CustomRegion, orientation, type_, leading, readingDirection,
                                                textLineOrder, readingOrientation, indented, align, primaryLanguage,
                                                secondaryLanguage, primaryScript, secondaryScript, production, TextLine,
                                                TextEquiv, TextStyle)


supermod.TextRegionType.subclass = TextRegionTypeSub


# end class TextRegionTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PcGtsType'
        rootClass = supermod.PcGtsType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=DefaultNamespace,
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PcGtsType'
        rootClass = supermod.PcGtsType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from io import BytesIO as StringIO
    parser = None
    rootNode = parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PcGtsType'
        rootClass = supermod.PcGtsType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=DefaultNamespace)
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PcGtsType'
        rootClass = supermod.PcGtsType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    main()
