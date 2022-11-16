import base64, json

def decode_file(xfile, gPath, sPath, binPath):
    # print(xfile)
    readFile = xfile['data'].encode('utf-8')
    print(readFile)
    encodedData = readFile
    
    binStore = open(gPath+binPath, 'wb')
    binStore.write(readFile)
    binStore.close()
    
    # decodedData = base64.b64decode((encodedData))
    
    imgFile = open(gPath+sPath, 'wb')
    imgFile.write(readFile)
    imgFile.close()
    
    return [imgFile, binStore]
    
# def 