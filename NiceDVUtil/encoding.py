import chardet
import codecs
import json


class EncodeFile(object):

    def __init__(self, options):
        self.options = options
        self.t0 = None

    def run(self):
        self.encode()

    def encode(self):
        info = {}
        #  Detect coding
        converted, coding = self.detectfileencoding(self.options.filename, self.options.coding)
        info['coding'] = coding

        #  If encoding is required,  converted will be set to true.
        if not converted:

            targetFileName = self.encodefile(self.options.filename, coding, self.options.coding)
            info['converted'] = True
            info['targetFileName'] = targetFileName

        else:
            info['converted'] = False
            info['targetFileName'] = self.options.filename

        # info['converted'] = False
        # info['targetFileName'] = self.options.filename


    @staticmethod
    def prependfile(sourceFileName, identifier=None, blocksize=10.49):
        targetFileName = sourceFileName[:(sourceFileName.rfind("."))] + '_' + 'uuid' + '.fhx'

        BLOCKSIZE = int(blocksize * 1000000)  # 1000000 bytes = 1mb
        with open(sourceFileName, "r") as sourceFile:
            with open(targetFileName, "w") as targetFile:
                if identifier is not None:
                    targetFile.write("/* {} */ \n".format(json.dumps(identifier)))

                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)

        return targetFileName

    @staticmethod
    def encodefile(sourceFileName, sourceCoding, targetCoding, blocksize=10.49):
        '''
        usage encodefile('PA2_03232015.fhx','UTF-16LE',ascii)
        '''

        targetFileName = sourceFileName[:(sourceFileName.rfind("."))]+'_'+targetCoding+'.fhx'

        # BLOCKSIZE = 10485760  # or some other, desired size in bytes = 10 mb
        BLOCKSIZE = int(blocksize*1000000)  # 1000000 bytes = 1mb
        with codecs.open(sourceFileName, "r", sourceCoding) as sourceFile:
            with codecs.open(targetFileName, "w", targetCoding) as targetFile:

                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)

        return targetFileName

    @staticmethod
    def detectfileencoding(file, targetEncoding):
        '''
        usage: detect_file_encoding('DeltaV_System.fhx','ascii')
        '''
        tmp = None
        with open(file, 'rb') as in_file:
            for line in in_file:
                tmp = chardet.detect(line)  # Returns Dic
                tmp = tmp['encoding']
                break
            if tmp == targetEncoding or tmp == 'ascii':
                return True, tmp
            else:
                return False, tmp


