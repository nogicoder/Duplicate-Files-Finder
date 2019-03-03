from os import chdir
from subprocess import run


def create_dir():
    try:
        run('mkdir duplicates/', shell=True)
        chdir('duplicates/')
        run('mkdir dir1', shell=True)
        chdir('dir1')
        run('mkdir dir2', shell=True)
        chdir('dir2')
        run('mkdir dir3', shell=True)
        chdir('../../')
        run('mkdir dir4', shell=True)
        run('mkdir dir5', shell=True)
        chdir('dir5')
        run('mkdir dir6', shell=True)
        chdir('../')
    except OSError:
        pass


def create_files():
    chdir('dir1')
    with open('test1', 'w+') as test1:
        test1.write('This is test1')
    chdir('dir2')
    with open('test1x', 'w+') as test1x:
        test1x.write('This is test1')
    chdir('dir3')
    with open('test2', 'w+') as test2:
        test2.write('This is test2')
    chdir('../../../dir4')
    with open('test2x', 'w+') as test2x:
        test2x.write('This is test2')
    chdir('../dir5')
    with open('test2xx', 'w+') as test2xx:
        test2xx.write('This is test2')
    chdir('dir6')
    with open('test3', 'w+') as test3:
        test3.write('This is test3')
    test4 = open('emptyfile.txt', 'w+')
    test4.close()


def main():
    create_dir()
    create_files()


if __name__ == '__main__':
    main()
