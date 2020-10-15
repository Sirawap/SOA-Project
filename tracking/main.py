from fastapi import FastAPI
import requests

result = dict()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
    return format
    {
        name: {
            edges: [],
            covidEdges: [],
        }
    }
"""


@app.get("/graph")
async def transform_graph():
    # r = requests.get("")
    # r_json = r.json()

    # r_json = {
    #     "a": {
    #         "b": 1,
    #         "c": 0
    #     }
    # }

    r_json = [
        {
            "contact": [
                {
                    "contact": "b",
                    "time": "14.30"
                }
            ],
            "covid": [
                {
                    "contact": "c",
                    "time": "14.30"
                }
            ],
            "id": "a"
        }
    ]

    for host in r_json:
        temp = {
            "normalEdges": list(),
            "covidEdges": list()
        }

        for person in host["contact"]:
            temp['covidEdges'].append(person['contact'])

        for person in host["covid"]:
            temp['normalEdges'].append(person['contact'])

        result[host['id']] = temp

    return result

    # for name, people in r_json.items():
    #     temp = {
    #         "edges": list(),
    #         "covidEdges": list()
    #     }

    #     for p_name, is_covid in people.items():
    #         temp['edges'].append(
    #             p_name) if is_covid else temp['covidEdges'].append(p_name)

    #     result[name] = temp

    # return result

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080)
