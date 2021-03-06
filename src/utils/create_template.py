"""
templateを作成する intaractive shell
"""
import codecs
from os import makedirs, path
from pathlib import Path

from config.datapath import PROJECT_TOP

TEMPLATE_COMMON_MESSAGE = "# generated by create_template.py\n"


def create_folder(folder_path):
    print("create_folder:", folder_path)
    makedirs(folder_path, exist_ok=True)


def read(filepath):
    with codecs.open(filepath, "r", "utf-8") as f:
        return f.read()


def write(filepath, content):
    with codecs.open(filepath, "w", "utf-8") as f:
        print("create_file:", filepath)
        f.write(content)


class FolderTemplate:
    def __init__(self, domain_name, dir_name, common_files, project_top=PROJECT_TOP,
                 template_common_message=TEMPLATE_COMMON_MESSAGE):
        self.dir_name = dir_name
        self.domain_name = domain_name
        self.common_files = common_files
        self.template_common_message = template_common_message
        temp = Path(project_top)
        self.src_dir = temp.joinpath("src")

    def create_blank_template(self, keep_existing_file=True):
        base_dir_path = self.src_dir.joinpath(self.dir_name, self.domain_name)
        makedirs(base_dir_path, exist_ok=True)
        for file in self.common_files:
            if path.exists(base_dir_path.joinpath(file)) and keep_existing_file:
                pass
            else:
                write(base_dir_path.joinpath(file), self.template_common_message)

    def create_template_from_sample(self, sample_domain_name, keep_existing_file=True):
        base_dir_path = self.src_dir.joinpath(self.dir_name, self.domain_name)
        sample_domain_path = self.src_dir.joinpath(self.dir_name, sample_domain_name)
        makedirs(base_dir_path, exist_ok=True)
        for file in self.common_files:
            content = self.template_common_message
            print(list(sample_domain_path.glob(file)))
            sample_file_globbed = list(sample_domain_path.glob(file))
            if len(sample_file_globbed) > 0:  # exists
                sample_source_code_path = list(sample_domain_path.glob(file))[0]
                source_code = read(sample_source_code_path)
                source_code = source_code.replace(sample_domain_name, self.domain_name).replace(
                    sample_domain_name.lower(), self.domain_name.lower())
                content = source_code

            if path.exists(base_dir_path.joinpath(file)) and keep_existing_file:
                pass
            else:
                write(base_dir_path.joinpath(file), content)

    def create(self, sample_domain_name=None, keep_existing_file=True):
        if sample_domain_name is not None:
            self.create_template_from_sample(sample_domain_name, keep_existing_file=keep_existing_file)
        else:
            self.create_blank_template(keep_existing_file=keep_existing_file)


class TemplateCreator:
    def __init__(self, domain_name):
        config = FolderTemplate(domain_name=domain_name, dir_name="config",
                                common_files=["__init__.py", "const.py", "datapath.py", "args.py"])
        data = FolderTemplate(domain_name=domain_name, dir_name="data",
                              common_files=["__init__.py", "data_manager.py", "preprocess.py", "data_module.py"])
        models = FolderTemplate(domain_name=domain_name, dir_name="models", common_files=["__init__.py", "model.py"])
        controller = FolderTemplate(domain_name=domain_name, dir_name="controllers",
                                    common_files=["__init__.py", "train_model.py", "evaluate_model.py", "predict.py"])

        self.common_project_structures = [config, data, models, controller]

    def create(self, sample_domain_name=None, keep_existing_file=True):
        for template in self.common_project_structures:
            template.create(sample_domain_name=sample_domain_name, keep_existing_file=keep_existing_file)


def ops(domain_name, sample_domain_name=None, keep_existing_file=True):
    template_creator = TemplateCreator(domain_name)
    template_creator.create(sample_domain_name=sample_domain_name, keep_existing_file=keep_existing_file)


def main():
    print("domain name:")
    domain_name = input()
    print("sample_domain")
    sample_name = input()
    ops(domain_name, sample_name)


if __name__ == '__main__':
    main()
