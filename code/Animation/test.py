from read_data import begin
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    a = begin()
    a.run()
    print(a.center)

# https://github.com/dipy/dipy/issues/399