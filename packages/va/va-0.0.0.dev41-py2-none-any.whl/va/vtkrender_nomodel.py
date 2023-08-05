import vtk


def main():
    """

        Produce surface views from X, y, Z directions. When model is there,
        model and map surface views for x, y, z directions were produced.


    :return: None
    """
    vtpFile = "2557.vtp"
    model = '4d2u.ent'
    #model = ''

    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(vtpFile)
    reader.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.ScalarVisibilityOff()
    mapper.SetInputConnection(reader.GetOutputPort())


    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 0.8, 0.1)
    actor.GetProperty().SetInterpolationToPhong()
    actor.GetProperty().SetDiffuse(0.9)
    actor.GetProperty().SetSpecular(0.6)
    actor.GetProperty().SetSpecularPower(30)
    actor.GetProperty().BackfaceCullingOn()
    actor.GetProperty().FrontfaceCullingOn()

    # Create the graphics structure. The renderer renders into the render
    # window. The render window interactor captures mouse events and will
    # perform appropriate camera or actor manipulation depending on the
    # nature of the events.

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1)
    renWin.SetSize(300, 300)
    renWin.AddRenderer(ren)

    # Add the actors to the renderer, set the background and size
    #actor.RotateY(90)
    ren.AddActor(actor)
    ren.SetBackground(0.9, 0.9, 0.9)
    ren.GetActiveCamera().SetParallelProjection(1)
    renWin.Render()

    # 
    #factGraphics = vtk.vtkGraphicsFactory()
    #factGraphics.SetUseMesaClasses(1)
    #factImage = vtk.vtkImagingFactory()
    #factImage.SetUseMesaClasses(1)

    # Model exist
    if model:
        actor.GetProperty().SetOpacity(0.5)
        pdb_reader = vtk.vtkPDBReader()
        model_mapper = vtk.vtkPolyDataMapper()
        model_actor = vtk.vtkActor()
        model_actor.GetProperty().SetLineWidth(11)
        pdb_reader.SetFileName(model)

        model_mapper.SetInputConnection(pdb_reader.GetOutputPort())
        model_actor.SetMapper(model_mapper)
        ren.AddActor(model_actor)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(0.55)
        renWin.Render()

        # Output model and maps overlay images
        write_image('testimageZ.bmp', renWin)

        actor.RotateX(90)
        actor.RotateY(90)
        model_actor.RotateX(90)
        model_actor.RotateY(90)
        #ren.ResetCamera()
        write_image('testimageY.bmp', renWin)

        actor.RotateZ(90)
        actor.RotateX(90)
        model_actor.RotateZ(90)
        model_actor.RotateX(90)
        #ren.ResetCamera()
        write_image('testimageX.bmp', renWin)


    else:
        # Ouput maps images only
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(0.55)
        write_image('testimageZ.bmp', renWin)

        actor.RotateX(90)
        actor.RotateY(90)
        #ren.ResetCamera()
        write_image('testimageY.bmp', renWin)

        actor.RotateZ(90)
        actor.RotateX(90)
        #ren.ResetCamera()
        write_image('testimageX.bmp', renWin)



    return None


def write_image(imageFile, renWin):
    # Write the current view of the renderer to an image
    if imageFile:
        writer = vtk.vtkBMPWriter()
        windowto_image_filter = vtk.vtkWindowToImageFilter()
        windowto_image_filter.SetInput(renWin)
        windowto_image_filter.SetScale(3)  # image quality
        windowto_image_filter.SetInputBufferTypeToRGB()

        writer.SetFileName(imageFile)
        writer.SetInputConnection(windowto_image_filter.GetOutputPort())
        writer.Write()
    else:
        raise RuntimeError('Need a filename.')


main()
