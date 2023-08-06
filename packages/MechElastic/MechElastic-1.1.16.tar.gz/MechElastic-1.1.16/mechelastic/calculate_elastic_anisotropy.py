from .comms import printer
from .parsers import VaspOutcar
from .parsers import AbinitOutput
from .core import ELATE


def calculate_elastic_anisotropy(
    infile="OUTCAR", code="vasp", plot=None, elastic_calc=None, ddbfile=None
):

    """
    This method calculates the elastic properties
    of a material from a DFT calculation. hi
    """

    # welcome message
    printer.print_mechelastic()

    elastic_tensor = None

    rowsList = []
    # calling parser
    if code == "vasp":

        output = VaspOutcar(infile=infile)
        elastic_tensor = output.elastic_tensor
        elastic_tensor = output.elastic_tensor
        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j],3))
            rowsList.append(columnsList)

    elif code == "abinit":
        output = AbinitOutput(infile=infile, ddbfile=ddbfile)
        elastic_tensor = output.elastic_tensor
        elastic_tensor = output.elastic_tensor
        row = elastic_tensor.shape[0]
        col = elastic_tensor.shape[1]
        rowsList = []
        for i in range(row):
            columnsList = []
            for j in range(col):
                columnsList.append(round(elastic_tensor[i, j],3))
            rowsList.append(columnsList)
    print(rowsList)
    elastic_tensor = ELATE.ELATE(rowsList)

    if plot == "2D":
        elastic_tensor.plot_2D(elastic_calc=elastic_calc)
    elif plot == "3D":
        elastic_tensor.plot_3D(elastic_calc=elastic_calc)

    elastic_tensor.print_properties()

    print("\nThanks! See you later. ")
    return output
