import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO
from getImage import drawStroke
from getTrans import geminiTrans
from getHint import gpto3Hint

def clearOldData(imageFolder, textFolder):

    # Clear all content in imageFolder
    if os.path.exists(imageFolder):
        for root, dirs, files in os.walk(imageFolder, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f'Error deleting {file_path}: {e}')
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f'Error removing directory {dir_path}: {e}')

    # Clear all content in textFolder
    if os.path.exists(textFolder):
        for root, dirs, files in os.walk(textFolder, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f'Error deleting {file_path}: {e}')
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f'Error removing directory {dir_path}: {e}')


if __name__ == "__main__":

    #Folders where we will store output images, hints and transcriptions
    imageFolder = 'testDataOut/images'
    txtFolder = 'testDataOut/text'
    clearOldData(imageFolder, txtFolder)

    #Load solution data
    solutionsAll = pd.read_csv('testDataIn/vladSolutions.csv') 
    #Load stroke data for solutions
    strokesAll = pd.read_json('testDataIn/vladStrokes.json')

    for i in solutionsAll.index:

        #Get solution data for current solution
        solutionId = solutionsAll['solutionId'][i]
        problemDescription = solutionsAll['problem'][i]
        correctAnswer = solutionsAll['correctAnswer'][i]
        userAnswer = solutionsAll['userAnswer'][i]
        #Get stroke data for current solution
        strokes = next((s for s in strokesAll['histories'] if s['credits']['solutionId'] == solutionsAll['solutionId'][i]), None)

        #Here we store the strokes of the image in the correct fromat for recreating image
        imgStrokes = []

        for k, points in enumerate(strokes['shapes']):
            
            #Get x/y coordinates of stroke points
            xCoords = [point[0] for point in points['points']]
            yCoords = [point[1] for point in points['points']]
            #This format will be the format of the stroke we recieve from FE
            strokePoints = {'x': xCoords, 'y': yCoords, 'index': k}
            imgStrokes.append(strokePoints)
        
        #Draw the image from strokes
        image = drawStroke(imgStrokes)
        #Get reference image from drawboard
        refImageResponse = requests.get(f'https://s3.eu-central-1.amazonaws.com/prod.solutions/{solutionsAll['drawingImageName'][i]}')
        refImage = Image.open(BytesIO(refImageResponse.content))

        #Generate transcription
        trans = geminiTrans(image, problemDescription, correctAnswer, userAnswer)   
        #Generate hint
        hint = gpto3Hint(trans, problemDescription, correctAnswer, userAnswer)

        #Store images, hints and transcriptions
        imgSubfolder = os.path.join(imageFolder, solutionId)
        if not os.path.exists(imgSubfolder):
            os.makedirs(imgSubfolder)
        image.save(os.path.join(imgSubfolder, f'image_{solutionId}.png'))
        refImage.save(os.path.join(imgSubfolder, f'ref_{solutionId}.png'))

        txtSubfolder = os.path.join(txtFolder, solutionId)
        if not os.path.exists(txtSubfolder):
            os.makedirs(txtSubfolder)
        with open(os.path.join(txtSubfolder, 'trans.txt'), 'w') as f:
            f.write(trans)
        with open(os.path.join(txtSubfolder, 'hint.txt'), 'w') as f:
            f.write(hint)

