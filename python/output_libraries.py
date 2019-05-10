#!/usr/bin/python

# constatant
requirements = 'requirements.txt'
licenses = 'packages_and_licenses.txt'
columns = ["pkg_name", "version", "license", "url"]

req_list = []
licenses_list = []


def get_requirements_name(filename=requirements):
    ret_list = []
    with open(filename, 'r') as f:
        data = f.read()
        data_list = data.split('\n')
        for d in data_list:
            ret_list.append(d[:d.find('=')].lower())
    return ret_list


def get_lib_name_and_license(target_lib, filename=licenses):
    ret_list = []
    with open(licenses, 'r') as f:
        data = f.read()
        data_list = data.split('\n')
        for d in data_list:
            split_data = d.split('\t')
            if split_data[0] in target_lib:
                ret_list.append(split_data)
    return ret_list


def list_to_json(data_list):
    json_data_list = []
    for data in data_list:
        json_data_list.append(
            {
                "pkg_name": data[0],
                "version": data[1],
                "license": data[2],
                "url": data[3]
            }
        )
    return json_data_list


def check_license(data_list):
    ok_list = []
    ng_list = []
    for data in data_list:
        if 'GPL' in data['license']:
            ng_list.append(data)
        else:
            ok_list.append(data)
    return ok_list, ng_list


if __name__ == '__main__':
    reqs = get_requirements_name()
    license_list = get_lib_name_and_license(reqs)
    license_list_json = list_to_json(license_list)
    ok_list, ng_list = check_license(license_list_json)
