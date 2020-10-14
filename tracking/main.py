from fastapi import FastAPI
import requests

app = FastAPI()

result = dict()


@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
    return 
    #1
    {
        nodeId: {
            name: "",
            edges: [],
            covidEdges: [],
        }
    }
    #2
    {
        name: {
            edges: [],
            covidEdges: [],
        }
    }
"""


# r_json = {
#     "a": {
#         "b": 1,
#         "c": 0
#     }
# }

# for name, people in r_json.items():
#     temp = {
#         "edges": list(),
#         "covidEdges": list()
#     }

#     for p_name, is_covid in people.items():
#         temp['edges'].append(
#             p_name) if is_covid else temp['covidEdges'].append(p_name)

#     result[name] = temp
#     print(result)


@app.get("/graph")
async def transform_graph():
    # r = requests.get("")
    # r_json = r.json()

    r_json = {
        "a": {
            "b": 1,
            "c": 0
        }
    }

    for name, people in r_json.items():
        temp = {
            "edges": list(),
            "covidEdges": list()
        }

        for p_name, is_covid in people.items():
            temp['edges'].append(
                p_name) if is_covid else temp['covidEdges'].append(p_name)

        result[name] = temp

    return result
