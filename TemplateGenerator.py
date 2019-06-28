#!/usr/bin/env python3
import os
import shutil
from distutils.dir_util import copy_tree


class TemplateGenerator:
    default_package = "id.example.mvp"
    template_pkg = "id.example.mvp"
    template_dir = template_pkg.replace(".", "/")

    def __init__(self, pkg_id, app_name):
        self.app_name = app_name
        self.package_id = pkg_id
        self.output_dir = "{}/{}".format("output", app_name)

    def do_generate(self):
        package_path = self.package_id.replace(".", "/")
        my_dir = os.getcwd()
        self.make_dir(self.package_id)
        os.chdir(my_dir)
        self.copy_template_files(self.package_id)
        self.copy_template_project(package_path)
        self.copy_template_res()

        os.chdir(my_dir)
        print("change package name to {}".format(self.package_id))
        self.replace_package_id(self.default_package, self.package_id)

    def replace_package_build_gradle(self, default_pkg, new_pkg):
        file_input = "build.gradle"
        filedata = None
        print("replace package id")
        x = "change {} to {}".format(default_pkg, new_pkg)
        print(x)
        with open(file_input, 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(self.default_package, self.package_id)

        with open(file_input, 'w') as file:
            file.write(filedata)

    def replace_package_id(self, def_pkg, new_pkg):
        path = "{}/{}".format(os.getcwd(), self.output_dir)
        print("path: {}".format(path))
        patterns = [".kt", ".xml"]

        matching_file_list = [os.path.join(dp, f)
                              for dp, dn, filenames in os.walk(path)
                              for f in filenames
                              if os.path.splitext(f)[1] in patterns]
        print('Files found matching patterns: ' + str(len(matching_file_list)))
        fileCount = 0
        filesReplaced = 0

        for currentFile in matching_file_list:

            fileCount += 1
            fileReplaced = self.replace_package_in_file(currentFile, def_pkg, new_pkg)
            if fileReplaced:
                filesReplaced += 1

        print("Total Files Searched         : " + str(fileCount))
        print("Total Files Replaced/Updated : " + str(filesReplaced))

    def replace_package_in_file(self, file_name, def_pkg, new_pkg):
        # print("change package id in file {}".format(file_name))
        file_updated = False

        with open(file_name, 'r') as f:
            new_lines = []
            for line in f.readlines():
                if def_pkg in line:
                    file_updated = True
                line = line.replace(def_pkg, new_pkg)
                new_lines.append(line)

        if file_updated:
            print("String found and update file {}".format(file_name))
            try:
                with open(file_name, 'w') as f:
                    for line in new_lines:
                        f.write(line)
            except:
                print("ERROR! Can't access file {}".format(file_name))

        return file_updated

    def make_dir(self, pkg_id):
        path = pkg_id.replace(".", "/")
        app_dir = "app/src"
        android_test_dir = "{}/{}".format("androidTest/java", path)
        main_dir = "{}/{}".format("main/java", path)
        test_dir = "{}/{}".format("test/java", path)
        res_dir = "main/res"

        print("path: {}".format(path))

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        else:
            print("path {} already exists".format(self.output_dir))

        # gradle directory
        if not os.path.exists("gradle/wrapper"):
            os.chdir(self.output_dir)
            os.makedirs("gradle/wrapper")

        print(os.getcwd())
        app = "{}/{}".format(self.output_dir, app_dir)
        if not os.path.exists(app):
            os.makedirs(app_dir)

        if not os.path.exists(main_dir):

            os.chdir(app_dir)
            print(os.getcwd())
            os.makedirs(main_dir)
            os.makedirs(res_dir)
            os.makedirs(android_test_dir)
            os.makedirs(test_dir)
        else:
            print("{} already created".format(main_dir))

    def copy_template_files(self, pkgId):

        # copy gradle stuff
        shutil.copyfile("template/build.gradle", "{}/{}".format(self.output_dir, "build.gradle"))
        shutil.copyfile("template/gradle.properties", "{}/{}".format(self.output_dir, "gradle.properties"))
        shutil.copyfile("template/gradlew", "{}/{}".format(self.output_dir, "gradlew"))
        shutil.copyfile("template/gradlew.bat", "{}/{}".format(self.output_dir, "gradlew.bat"))
        shutil.copyfile("template/settings.gradle", "{}/{}".format(self.output_dir, "settings.gradle"))

        #  copy wrapper
        shutil.copyfile("template/gradle/wrapper/gradle-wrapper.jar",
                        "{}/{}".format(self.output_dir, "gradle/wrapper/gradle-wrapper.jar"))
        shutil.copyfile("template/gradle/wrapper/gradle-wrapper.properties",
                        "{}/{}".format(self.output_dir, "gradle/wrapper/gradle-wrapper.properties"))

        # copy gradle app
        shutil.copyfile("template/app/build.gradle", "{}/{}".format(self.output_dir, "app/build.gradle"))
        shutil.copyfile("template/app/dependencies.gradle", "{}/{}".format(self.output_dir, "app/dependencies.gradle"))
        shutil.copyfile("template/app/proguard-rules.pro", "{}/{}".format(self.output_dir, "app/proguard-rules.pro"))

    def copy_template_project(self, pkg_path):

        copy_tree(
            "{}/{}".format("template/app/src/androidTest/java", self.template_dir),
            "{}/{}/{}".format(self.output_dir, "app/src/androidTest/java", pkg_path)
        )

        copy_tree(
            "{}/{}".format("template/app/src/main/java", self.template_dir),
            "{}/{}/{}".format(self.output_dir, "app/src/main/java", pkg_path)
        )

        copy_tree(
            "{}/{}".format("template/app/src/test/java", self.template_dir),
            "{}/{}/{}".format(self.output_dir, "app/src/test/java", pkg_path)
        )

    def copy_template_res(self):
        copy_tree(
            "{}".format("template/app/src/main/res"),
            "{}/{}".format(self.output_dir, "app/src/main/res")
        )


if __name__ == "__main__":
    my_app_name = "MyApp"
    my_pkg_id = "id.pkg.mvp"
    generator = TemplateGenerator(pkg_id=my_pkg_id, app_name=my_app_name)
    generator.do_generate()
