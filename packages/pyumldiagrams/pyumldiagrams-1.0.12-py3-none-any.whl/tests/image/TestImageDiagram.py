
from logging import Logger
from logging import getLogger
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions

from pyumldiagrams.image.ImageDiagram import ImageDiagram
from pyumldiagrams.image.ImageFormat import ImageFormat

from tests.TestBase import TestBase
from tests.TestConstants import TestConstants
from tests.TestDiagramParent import TestDiagramParent


class TestImageDiagram(TestDiagramParent):

    CELL_WIDTH:  int = 150  # pixels
    CELL_HEIGHT: int = 100  # pixels

    TEST_LAST_X_POSITION: int = 5
    TEST_LAST_Y_POSITION: int = 6

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestImageDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestImageDiagram.clsLogger

    def tearDown(self):
        pass

    def testBasicDiagramDraw(self):

        diagram:  ImageDiagram    = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-Basic.{ImageFormat.PNG.value}')
        classDef: ClassDefinition = ClassDefinition(name=TestDiagramParent.BASE_TEST_CLASS_NAME,
                                                    size=Size(width=266, height=100),
                                                    position=Position(x=107, y=30)
                                                    )

        diagram.drawClass(classDef)
        diagram.write()

    def testFillPage(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-Full.{ImageFormat.PNG.value}')

        widthInterval:  int = TestImageDiagram.CELL_WIDTH // 10
        heightInterval: int = TestImageDiagram.CELL_HEIGHT // 10

        for x in range(0, TestImageDiagram.TEST_LAST_X_POSITION):
            scrX: int = (x * TestImageDiagram.CELL_WIDTH) + (widthInterval * x)

            for y in range(0, TestImageDiagram.TEST_LAST_Y_POSITION):

                scrY: int = (y * TestImageDiagram.CELL_HEIGHT) + (y * heightInterval)
                classDef: ClassDefinition = ClassDefinition(name=f'{TestImageDiagram.BASE_TEST_CLASS_NAME}{x}{y}',
                                                            position=Position(scrX, scrY),
                                                            size=Size(width=TestImageDiagram.CELL_WIDTH, height=TestImageDiagram.CELL_HEIGHT))
                diagram.drawClass(classDef)

        diagram.write()

    def testBasicMethod(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'Test-BasicMethod.png')

        position: Position = Position(107, 30)
        size:     Size     = Size(width=266, height=100)

        car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        initParam: ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')
        initMethodDef.parameters = [initParam]
        car.methods = [initMethodDef]

        diagram.drawClass(car)

        diagram.write()

    def testBasicMethods(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-BasicMethods.{ImageFormat.PNG.value}')

        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testBasicHeader(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-BasicHeader.{ImageFormat.PNG.value}',
                                             headerText=TestDiagramParent.UNIT_TEST_HEADER)
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testSophisticatedHeader(self):
        from time import localtime

        from time import strftime

        today = strftime("%d %b %Y %H:%M:%S", localtime())

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-SophisticatedHeader.{ImageFormat.PNG.value}',
                                             headerText=f'{TestDiagramParent.UNIT_TEST_SOPHISTICATED_HEADER} - {today}')
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)

        diagram.write()

    def testSophisticatedLayout(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-SophisticatedLayout.{ImageFormat.PNG.value}')

        classDefinitions: ClassDefinitions = [
            self._buildCar(),
            self._buildCat(),
            self._buildOpie(),
            self._buildNameTestCase(),
            self._buildElectricCar()
        ]
        for classDefinition in classDefinitions:
            classDefinition = cast(ClassDefinition, classDefinition)
            diagram.drawClass(classDefinition=classDefinition)

        lineDefinitions: UmlLineDefinitions = self._buildSophisticatedLineDefinitions()
        for lineDefinition in lineDefinitions:
            diagram.drawUmlLine(lineDefinition=lineDefinition)

        diagram.write()

    def testMinimalInheritance(self):

        diagram: ImageDiagram = ImageDiagram(fileName=f'{TestConstants.TEST_FILE_NAME}-MinimalInheritance.{ImageFormat.PNG.value}')

        cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        diagram.drawClass(classDefinition=cat)
        diagram.drawClass(classDefinition=opie)

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, source=Position(600, 208), destination=Position(600, 93))

        diagram.drawUmlLine(lineDefinition=opieToCat)
        diagram.write()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestImageDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
