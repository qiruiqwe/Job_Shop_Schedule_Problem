import csv

class Solution:

    def __init__(self, operationList=None):
        self._operationList = [] if operation is None else operationList

    def insertOperation(self, index, Operation):
        self._operationList.insert(index, Operation)

    def removeOperationAt(self, index):
        return self._operationList.pop(index)

    def getOperationAt(self, index):
        return self._operationList[index]

    # def createSchedule(self):
        # TODO


class task:

    def __init__(self, jobId, taskId, sequence, usableMachines, pieces):
        self._jobId = jobId
        self._taskId = taskId
        self._sequence = sequence
        self._usableMachines = usableMachines
        self._pieces = pieces

    def getJobId(self):
        return self._jobId

    def getTaskId(self):
        return self._taskId

    def getSequence(self):
        return self._sequence

    def getUsableMachines(self):
        return self._usableMachines

    def getPieces(self):
        return self._pieces

    def printTask(self):
        print("[{}, {}, {}, {}, {}]".format(self._jobId,
                                            self._taskId,
                                            self._sequence,
                                            self._usableMachines,
                                            self._pieces))


class job:

    def __init__(self, jobId):
        self._jobId = jobId
        self._tasks = []

    def getTask(self, taskId):
        return self._tasks[taskId]

    def getJobId(self):
        return self._jobId


class operation:

    def __init__(self, task, machine):
        self._task = task
        self._machine = machine

    def getTask(self):
        return self._task

    def getMachine(self):
        return self._machine

    def setMachine(self, machineId):
        self._machine = machineId

    def getString(self):
        return "[{}, {}, {}, {}]".format(self._task.getJobId(),
                                         self._task.getTaskId(),
                                         self._task.getSequence(),
                                         self._machine)

class data:
    # create sequenceDependencyMatrix
    sequenceDependencyMatrix = []

    # create dictionary for sequenceDependencyMatrix getSetupTime()
    dependencyMatrixIndexEncoding = {}

    # create mapping of {jobId : job}
    jobs = {}

    # create list of machine speeds
    machineSpeeds = []

    # populates data.jobs by reading jobTaskcsv
    # and populates data.indexEncoding (i.e {(jobId, taskId) : index}) for sequenceDependencyMatrix
    #
    # Note: indexEncoding is used in getSetupTime()
    @staticmethod
    def readjobTasksFile(inputFile):
        prevJobId = -1  # previously seen job
        index = 0       # used for mapping (jobId, taskId) : index in dependencyMatrixIndexEncoding
        with open(inputFile) as fin:
            # skip headers (i.e. first row in csv file)
            next(fin)
            for row in csv.reader(fin):
                # create task object
                tmpTask = task(
                    int(row[0]),
                    int(row[1]),
                    int(row[2]),
                    [int(x) for x in row[3][1:-1].split(' ')],
                    int(row[4])
                )
                # create & append new job if we encounter jobId that has not been seen
                if tmpTask._jobId != prevJobId:
                    data.jobs[tmpTask._jobId] = job(tmpTask._jobId)
                    prevJobId = tmpTask._jobId

                # append task to associated job.tasks list
                data.jobs[tmpTask._jobId]._tasks.append(tmpTask)

                # add mapping task : index to dependencyMatrixIndexEncoding dictionary
                data.dependencyMatrixIndexEncoding[tmpTask] = index
                index += 1

    # populates data.sequenceDependencyMatrix by reading sequenceDependencyMatrixcsv
    @staticmethod
    def readsequenceDependencyMatrixFile(inputFile):
        with open(inputFile) as fin:
            # skip headers (i.e. first row in csv file)
            next(fin)
            for row in csv.reader(fin):
                data.sequenceDependencyMatrix.append([int(x) for x in row[1:]])

    # populates data.machineSpeeds by reading machineSeedscsv
    @staticmethod
    def readmachineSpeedsFile(inputFile):
        with open(inputFile) as fin:
            # skip headers (i.e. first row in csv file)
            next(fin)
            for row in csv.reader(fin):
                data.machineSpeeds.append(int(row[1]))

    @staticmethod
    def getSetupTime(prevTask, curTask):
        return data.sequenceDependencyMatrix[data.dependencyMatrixIndexEncoding[prevTask]][
            data.dependencyMatrixIndexEncoding[curTask]] if prevTask != None else 0


    @staticmethod
    def getJob(jobId):
        return data.jobs[jobId]

    @staticmethod
    def getMachineSpeed(machineId):
        return data.machineSpeeds[machineId]

    @staticmethod
    def getNumerOfMachines():
        return len(data.machineSpeeds)

    @staticmethod
    def getNumberOfJobs():
        return len(data.jobs)

    @staticmethod
    def printData():
        print("JobTasks:\n")
        print("  [jobId, taskId, sequence, usable_machines, pieces]\n")
        for job in data.jobs:
            for task in job._tasks:
                print("  ", end="")
                task.printTask()

        print("\nSequenceDependencyMatrix:\n")
        for row in data.sequenceDependencyMatrix:
            print("  ", end="")
            print(row)

        print("\nDependencyMatrixIndexEncoding:\n")
        print("  (jobId, taskId) : index\n")
        for key in data.dependencyMatrixIndexEncoding:
            print("  ", end="")
            print(f"{key} : {data.dependencyMatrixIndexEncoding[key]}")

        print("\nMachineSpeeds:\n")
        print("  machine : speed\n")
        for machine, speed in enumerate(data.machineSpeeds):
            print("  ", end="")
            print(f"{machine} : {speed}")

    @staticmethod
    def readDataFromFiles(seqDepMatrixFile, machineRunspeedsFile, jobTasksFile):
        data.readsequenceDependencyMatrixFile(seqDepMatrixFile)
        data.readmachineSpeedsFile(machineRunspeedsFile)
        data.readjobTasksFile(jobTasksFile)
