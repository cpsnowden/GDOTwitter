from AnalysisEngine.Graphing.Gephi.GephiRPC import GephiRpcClient
import json
from shutil import copyfile

def test(path,n):

    f_name = path + ".graphml"
    out = path + "_toolkit_" + str(n) + ".dat"


    params = {"LAYOUT_ITERATIONS": 1000,
              "LAYOUT_ALGO": "FA2MS",
              "THREADS_COUNT":n}

    client = GephiRpcClient()

    results = client.call(json.dumps({"GephiParameters": params,
                            "fileName": f_name}))

    print results

    copyfile("/Users/ChrisSnowden/IndividualProject/GDOTwitter/gephi/Performance_" + f_name  + ".dat",
             out)



test("TEST_10000",7)
# test("TEST_10000",5)
# test("TEST_10000",3)
# test("TEST_10000",1)
