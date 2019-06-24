#!/usr/bin/env python3
import os
import shutil
from distutils.dir_util import copy_tree


class TemplateGenerator:

	defaultPackage = "id.example.mvp"
	templatePkg = "id.example.mvp"
	templateDir = templatePkg.replace(".","/")

	def __init__(self, pkgId, appName):
		self.appName = appName
		self.packageId = pkgId
		self.outputDir = "{}/{}".format("output", appName)

	def doGenerate(self):
		packagePath = self.packageId.replace(".", "/")
		# self.makeDir(self.packageId)
		self.copyFiles(self.packageId)
		self.copyTemplateProject(packagePath)

	def replacePackageBuildGradle(self, defaultPkg, newPkg):
		fileInput = "build.gradle"
		filedata = None
		print("replace package id")
		x = ("change {} to {}").format(defaultPkg, newPkg)
		print(x)
		with open(fileInput, 'r') as file:
			filedata = file.read()
		
		filedata = filedata.replace(self.defaultPackage, self.packageId)
		

		with open(fileInput, 'w') as file:
			file.write(filedata)


	def replacePakgInFile(self, fileName, defPkg, newPkg):
		print("change package id in AndroidManifest")


	def makeDir(self, pkgId):
		path=pkgId.replace(".","/")
		appDir = "app/src"
		androidTestDir = "{}/{}".format("androidTest/java", path)
		mainDir = "{}/{}".format("main/java", path)
		testDir = "{}/{}".format("test/java", path)
		
		print("path: {}".format(path))
		
		if not os.path.exists(self.outputDir):
			os.mkdir(self.outputDir)
		else :
			print("path {} already exists".format(self.outputDir))

		# gradle directory
		if not os.path.exists("gradle/wrapper"):
			os.chdir(self.outputDir)
			os.makedirs("gradle/wrapper")
		
		print(os.getcwd())
		app = "{}/{}".format(self.outputDir, appDir)
		if not os.path.exists(app):
			os.makedirs(appDir)
		
		if not os.path.exists(mainDir):

			os.chdir(appDir)
			print(os.getcwd())
			os.makedirs(mainDir)
			os.makedirs(androidTestDir)
			os.makedirs(testDir)
		else:
			print("{} already created".format(mainDir))

		
	def copyFiles(self, pkgId):

		# copy gradle stuff
		shutil.copyfile("template/build.gradle", "{}/{}".format(self.outputDir, "build.gradle"))
		shutil.copyfile("template/gradle.properties", "{}/{}".format(self.outputDir, "gradle.properties"))
		shutil.copyfile("template/gradlew", "{}/{}".format(self.outputDir, "gradlew"))
		shutil.copyfile("template/gradlew.bat", "{}/{}".format(self.outputDir, "gradlew.bat"))
		shutil.copyfile("template/settings.gradle", "{}/{}".format(self.outputDir, "settings.gradle"))

		#  copy wrapper
		shutil.copyfile("template/gradle/wrapper/gradle-wrapper.jar", "{}/{}".format(self.outputDir, "gradle/wrapper/gradle-wrapper.jar"))
		shutil.copyfile("template/gradle/wrapper/gradle-wrapper.properties", "{}/{}".format(self.outputDir, "gradle/wrapper/gradle-wrapper.properties"))

		# copy gradle app
		shutil.copyfile("template/app/build.gradle", "{}/{}".format(self.outputDir, "app/build.gradle"))
		shutil.copyfile("template/app/dependencies.gradle", "{}/{}".format(self.outputDir, "app/dependencies.gradle"))
		shutil.copyfile("template/app/proguard-rules.pro", "{}/{}".format(self.outputDir, "app/proguard-rules.pro"))
	
	def copyTemplateProject(self, pkgPath):

		copy_tree(
			"{}/{}".format("template/app/src/androidTest/java", self.templateDir),
			"{}/{}/{}".format(self.outputDir,"app/src/androidTest/java",pkgPath)
		)

		copy_tree(
			"{}/{}".format("template/app/src/main/java", self.templateDir),
			"{}/{}/{}".format(self.outputDir,"app/src/main/java",pkgPath)
		)

		copy_tree(
			"{}/{}".format("template/app/src/test/java", self.templateDir),
			"{}/{}/{}".format(self.outputDir,"app/src/test/java",pkgPath)
		)

				

if __name__ == "__main__":
	myAppName = "MyApp"
	myPkgId = "id.pkg.mvp"
	generator = TemplateGenerator(pkgId = myPkgId, appName = myAppName)
	generator.doGenerate()