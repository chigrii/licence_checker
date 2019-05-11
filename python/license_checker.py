#!/usr/bin/python
import pkg_resources
import csv
import os

# constatant
requirements = 'requirements.txt'
result_list_name = 'pip_lib_licenses.csv'
csv_save_dir = 'result'
columns = ["pkg_name", "version", "license", "url"]


# export to csv.
# notice: expected datas type 2-dimensional list
def export_csv(filename, datas):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(columns)
        writer.writerows(datas)
    print("Export csv data. filename: {}".format(filename))


def get_pkg_list():
    return sorted(pkg_resources.working_set, key=lambda x: str(x).lower())


# get pkg license
def get_pkg_license(pkg):
    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    license = 'UNKNOWN'
    labels = ['License: ', 'Classifier: License :: OSI Approvesd ::']
    for label in labels:
        for line in lines:
            if line.startswith(label):
                license = line[len(label):]
                break
        if license != 'UNKNOWN':
            return license
    return '(License not found)'


# get pkg home page url
def get_pkg_home_page(pkg):
    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')
    label = 'Home-page: '
    url = ''
    for line in lines:
        if line.startswith(label):
            url = line[len(label):]
            break
    if url == 'UNKNOWN':
        url = 'https://pypi.python.org/pypi/' + pkg.key
    return url


def get_pkg_info_list():
    print("Get pkg info list...")
    pkgs = get_pkg_list()
    info_lists = []

    for pkg in pkgs:
        license_type = ''
        url = ''
        license_type = get_pkg_license(pkg)
        url = get_pkg_home_page(pkg)
        info = [pkg.key.strip(), pkg.version.strip(), license_type.strip(), url.strip()]
        info_lists.append(info)

    return info_lists

def license_check():
    # get pkg info lists
    info_lists = get_pkg_info_list()

    # export to './data' dir. type: csv
    if not csv_save_dir in os.listdir('.'):
        print("Create: save dir {}".format(csv_save_dir))
        os.makedirs(csv_save_dir)

    save_path = './{}/{}'.format(csv_save_dir, result_list_name)

    export_csv(save_path, info_lists)


if __name__ == '__main__':
    license_check()