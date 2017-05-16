import numpy as np
import math

def readToMatrix(dataFile):
	firstLine = dataFile.readline()
	categories = [a.strip('"') for a in list(firstLine.split(","))]

	A = np.matrix(list(dataFile.readline().split(",")))
	for line in dataFile:
		A = np.vstack([A, list(line.split(","))])

	return categories, A

#H(p, q) = ...
def entropy(p, q):
	if p == 0 or q == 0:
		return 1.0
	return - p * math.log(p, 2) - q * math.log(q, 2)

def main():
	dataFile = open('data.csv', 'r')
	categories, data = readToMatrix(dataFile)

	DIAGNOSIS_COL = 1
	
	


	diagnoses = data[ : , DIAGNOSIS_COL]
	initialBenignCount = len([currentDiagnosis for currentDiagnosis in diagnoses if currentDiagnosis == "B"])
	initialMalignantCount = len([currentDiagnosis for currentDiagnosis in diagnoses if currentDiagnosis == "M"])

	categoryIndex = 2
	print("Category\tSplit\tTotal<=\tB=<\tM=<\tTotal>\tB>\tM>\tH(old)\tH(new)\tGain\n")
	for currentRow in range(0, data.shape[0]): #Num of elems in dim 0(aka num of rows)
		currentValue = data[currentRow, categoryIndex]


		benignCountLess = len([currentDiagnosis for i, currentDiagnosis in enumerate(diagnoses) if currentDiagnosis == "B" and data[i, categoryIndex] <= currentValue])
		malignantCountLess = len([currentDiagnosis for i, currentDiagnosis in enumerate(diagnoses) if currentDiagnosis == "M" and data[i, categoryIndex] <= currentValue])
		totalLess = benignCountLess + malignantCountLess
		probBenignLess = benignCountLess / float(totalLess)
		probMalignantLess = benignCountLess / float(totalLess)

		benignCountGreater = len([currentDiagnosis for i, currentDiagnosis in enumerate(diagnoses) if currentDiagnosis == "B" and data[i, categoryIndex] > currentValue])
		malignantCountGreater = len([currentDiagnosis for i, currentDiagnosis in enumerate(diagnoses) if currentDiagnosis == "M" and data[i, categoryIndex] > currentValue])
		totalGreater = benignCountGreater + malignantCountGreater
		probBenignGreater = benignCountGreater / float(totalGreater)
		probMalignantGreater = benignCountGreater / float(totalGreater)

		total = totalLess + totalGreater
		probLess = totalLess / float(total)
		probGreater = totalGreater / float(total)

		pOld = initialBenignCount / float(initialBenignCount + initialMalignantCount)
		qOld = initialMalignantCount / float(initialBenignCount + initialMalignantCount)

		entropyOld = entropy(pOld, qOld)
		entropyNew = probLess * entropy(probBenignLess, probMalignantLess) + probGreater * entropy(probBenignGreater, probMalignantGreater)

		gain = entropyOld - entropyNew

		print(categories[categoryIndex] + "\t" + str(currentValue) + "\t" + 
			str(totalLess) + "\t" + str(benignCountLess) + "\t" + str(malignantCountLess) + "\t" +
			str(totalGreater) + "\t" + str(benignCountGreater) + "\t" + str(malignantCountGreater) + "\t" +
			str(entropyOld) + "\t" + str(entropyNew) + "\t" + str(gain))

		# print("There are " + str(benignCountUnderCurValue) + " benign under " + categories[categoryIndex] + str(currentValue))
		# print("There are " + str(malignantCountUnderCurValue) + " malignant under " + categories[categoryIndex] + str(currentValue))

		# pUnder = 
		# totalCount = benignCountUnderCurValue + malignantCountUnderCurValue
		# benignRatio = benignCountUnderCurValue / float(totalCount)
		# malignantRatio = malignantCountUnderCurValue / float(totalCount)
		# # print("benignRatio = " + str(benignRatio) + ", malignantRatio = " + str(malignantRatio))
		# if benignRatio == 0 or malignantRatio == 0:
		# 	h = 1.0
		# else:
		# 	h = - benignRatio * math.log(benignRatio, 2) - malignantRatio * math.log(malignantRatio, 2)

		# print(categories[categoryIndex] + "\t" + str(currentValue) + "\t\t" + str(totalCount) + "\t" + str(benignCountUnderCurValue) + "\t" + str(malignantCountUnderCurValue) + "\t" + str(h))
		# print("H(...) = " + str(h) + "\n")

		

main()
