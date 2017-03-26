class MakefileGenerator():

	def __init__(self, strip, workDir):
		self.strip = strip
		self.workDir = workDir

	def generatePanelBalloonsRules(self, panel, panelCounter):
		balloonCounter = 1
		for balloon in panel.balloonList:
			targetPosName = self.workDir + "/panel" + str(panelCounter) + "_balloon" + str(balloonCounter) + "_pos.png"
			targetName = self.workDir + "/panel" + str(panelCounter) + "_balloon" + str(balloonCounter) + ".png"
			targetSVGName = self.workDir + "/panel" + str(panelCounter) + "_balloon" + str(balloonCounter) + ".svg"

			posCommand = "./scripts/pos.sh $< " + str(balloon.position[0]) + " " + str(balloon.position[1]) + " " + str(panel.width) + " " + str(panel.height) + " $@"

			svgCommand = "./scripts/balloon.py -x 0 -y 0 -offset " + str(balloon.offset) +  " -bx " + str(balloon.orientation[0]) + "  -by " + str(balloon.orientation[1]) + " -c " + balloon.speech + " > $@"

			self.printMakefileRule(targetPosName, [targetName], [posCommand])
			self.printMakefileRule(targetSVGName, [""], [svgCommand])

			balloonCounter += 1

	def generatePanelRules(self):
		panelCounter = 1

		commands = ["./scripts/stack.sh $^ $@", "convert $@ -bordercolor black -compose Copy -border 5 -bordercolor white -compose Copy -border 20 $@"]

		for panel in self.strip.panelList:
			target = self.workDir + "/panel" + str(panelCounter) + ".png"

			dependancies = []
			for panelItem in panel.panelItemList:
				dependancies.append(panelItem.imageName)

			balloonCounter = 1
			for balloon in panel.balloonList:
				dependancies.append(self.workDir + "/panel" + str(panelCounter) + "_balloon" + str(balloonCounter) + "_pos.png")
				balloonCounter += 1

			self.generatePanelBalloonsRules(panel, panelCounter)

			self.printMakefileRule(target, dependancies, commands)
			panelCounter += 1

	def generateStripRule(self):
		target = self.workDir + "/strip.png"

		dependancies = []
		i = 1
		for panel in self.strip.panelList:
			dependancies.append(self.workDir + "/panel" + str(i) + ".png")
			i += 1

		commands = ["convert -append $^ $@"]

		self.printMakefileRule(target, dependancies, commands)

	def generateMakefile(self):
		self.printGenericRules()
		self.generateStripRule()
		self.generatePanelRules()

	def printMakefileRule(self, target, dependancies, commands):
		print(target + " : ", end = "")
		dependancyIndentation = " " * (len(target) + 3)
		first = True
		dependanciesNumber = len(dependancies)
		counter = 0
		for d in dependancies:
			if first:
				first = False
			else:
				print(dependancyIndentation, end="")
			print(d + " ", end="")

			counter += 1
			if counter != dependanciesNumber:
				print(" \\")
		print()
		for c in commands:
			print("\t" + c)
		print()

	def printGenericRules(self):
		self.printMakefileRule("%.png", ["%.svg"], ["convert $< $@"])
