
from typing import Any
from typing import List
from typing import Union
from typing import final

from logging import Logger
from logging import getLogger

from PIL.ImageDraw import ImageDraw

from pyumldiagrams.image.ImageCommon import ImageCommon
from pyumldiagrams.IDiagramLine import IDiagramLine
from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import UmlLineDefinition

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import InternalPosition


class ImageLine(IDiagramLine):

    DEFAULT_LINE_COLOR: final = 'Black'
    LINE_WIDTH:         final = 1

    PolygonPoints = List[float]

    def __init__(self, docWriter: Any, diagramPadding: DiagramPadding):

        super().__init__(docMaker=docWriter, diagramPadding=diagramPadding, dpi=0)

        self.logger: Logger = getLogger(__name__)

        self._imgDraw: ImageDraw = docWriter

    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter

        Args:
            lineDefinition:  Describes the line to draw
        """
        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritanceArrow(src=source, dest=destination)
        elif lineType == LineType.Composition:
            self._drawCompositionSolidDiamond(src=source, dest=destination)
        elif lineType == LineType.Aggregation:
            self._drawAggregationDiamond(src=source, dest=destination)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, src: Position, dest: Position):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert to points from screen coordinates
        Draw the arrow first
        Compute the mid point of the bottom line of the arrow
        That is where the line ends

        Args:
            src: start of line
            dest: end line line;  Arrow positioned here
        """
        internalSrc:  InternalPosition = self.__toInternal(src)
        internalDest: InternalPosition = self.__toInternal(dest)

        points:  ArrowPoints             = ImageCommon.computeTheArrowVertices(internalSrc, internalDest)
        polygon: ImageLine.PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newEndPoint: InternalPosition = ImageCommon.computeMidPointOfBottomLine(points[0], points[2])

        x1 = internalSrc.x
        y1 = internalSrc.y
        x2 = newEndPoint.x
        y2 = newEndPoint.y

        xy = [x1, y1, x2, y2]

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def _drawCompositionSolidDiamond(self, src: Position, dest: Position):

        internalSrc:  InternalPosition = self.__toInternal(src)
        internalDest: InternalPosition = self.__toInternal(dest)

        points:  DiamondPoints           = ImageCommon.computeDiamondVertices(internalSrc, internalDest)
        polygon: ImageLine.PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newEndPoint: InternalPosition = points[3]

        x1 = internalSrc.x
        y1 = internalSrc.y
        x2 = newEndPoint.x
        y2 = newEndPoint.y

        xy = [x1, y1, x2, y2]

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def _drawAggregationDiamond(self, src: Position, dest: Position):

        internalSrc:  InternalPosition = self.__toInternal(src)
        internalDest: InternalPosition = self.__toInternal(dest)

        points:  DiamondPoints           = ImageCommon.computeDiamondVertices(internalSrc, internalDest)
        polygon: ImageLine.PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR, fill='black')

        newEndPoint: InternalPosition = points[3]

        x1 = internalSrc.x
        y1 = internalSrc.y
        x2 = newEndPoint.x
        y2 = newEndPoint.y

        xy = [x1, y1, x2, y2]

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def __toInternal(self, position: Position) -> InternalPosition:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        iPos: InternalPosition = ImageCommon.toInternal(position, verticalGap=verticalGap, horizontalGap=horizontalGap)

        return iPos

    def __toPolygonPoints(self, points: Union[ArrowPoints, DiamondPoints]) -> PolygonPoints:

        polygon: ImageLine.PolygonPoints = []

        for point in points:
            polygon.append(int(point.x))
            polygon.append(int(point.y))

        return polygon
