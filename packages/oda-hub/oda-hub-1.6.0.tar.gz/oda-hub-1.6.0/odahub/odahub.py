import json
import os
import requests
import time
import base64
import urllib.parse
from collections import OrderedDict

from oda.exceptions import WorkflowIncomplete

from io import BytesIO
import rdflib

from odakb.sparql import load_graph


def get_default_graphs(rG):
    graphs = []


    for odahub_workflow in "oda-image", "integral-visibility", "integral-observation-summary":
        url_base = "https://oda-workflows-{}.odahub.io".format(odahub_workflow)
        graphs.append(url_base + "/api/v1.0/rdf")
    
        G = rdflib.Graph()

        print("will load", graphs[-1])
        load_graph(G, graphs[-1])

        for w in G.query("SELECT ?w WHERE { ?w rdfs:subClassOf anal:WebDataAnalysis }"):
            wns, wn = w[0].toPython().split("#")

            print("in found", odahub_workflow, wn)
            graphs.append("an:"+wn+" an:url \""+url_base+"/api/v1.0/get/"+wn+"\" .")
            graphs.append("an:"+wn+" an:odahubService \""+odahub_workflow+"\" .")
            graphs.append("an:"+wn+" rdfs:subClassOf an:odahubService .")
            graphs.append("an:odahubService rdfs:subClassOf an:Workflow .")
            graphs.append("an:"+wn+" rdfs:subClassOf oda:Workflow .")

    for graph in graphs:
        print("loading default graph", graph)
        load_graph(rG, graph)
        #open("{}.ttl".format(wn), "w").write(graphs[-1])

    return graphs

def get_workflow_url(workflow):
    print('exploiting workflow routes', os.environ.get('WORKFLOW_ROUTES',''))

    if os.environ.get('WORKFLOW_ROUTES'):
        workflow_routes = dict([ r.split("=") for r in os.environ.get('WORKFLOW_ROUTES','').split(",") ])
    else:
        workflow_routes = {}

    if workflow in workflow_routes:
        return workflow_routes[workflow]+"/api/v1.0/get/{}"

    if workflow in os.environ.get('STAGING_WORKFLOWS','').split(','):
        return "https://oda-workflows-"+workflow+"-staging.odahub.io/api/v1.0/get/{}"
    else:
        return "https://oda-workflows-"+workflow+".odahub.io/api/v1.0/get/{}"


def get_auth():
    for m in [
        lambda :open("/cdci-resources/reproducible").read().strip(),
        lambda :open(os.path.join(os.environ.get("HOME"),".reproducible")).read().strip(),
    ]:
        try:
            return requests.auth.HTTPBasicAuth("cdci", m())
        except:
            pass

def evaluate_retry(*args, **kwargs):
    ntries = kwargs.pop('ntries', 10)
    retry_wait = kwargs.pop('retry_wait', 5)

    for itry in range(ntries):
        try:
            return evaluate(*args, **kwargs)
        except Exception as e:
            print("not ready", e)
            time.sleep(retry_wait)

    raise Exception("unable to evaluate!")

def evaluate_dashboard(*args, **kwargs):
    return evaluate(*args, **{**kwargs, '_reroute_dashboard': True})

def evaluate(*args, **kwargs):
    reroute_dashbord = kwargs.pop('_reroute_dashboard', False)

    print("rd", reroute_dashbord)

    kwargs['_async_request'] = 'yes'
    url_template = get_workflow_url(args[0])

    url = url_template.format(*args[1:])
    print("url:",url)

    print("towards",url,kwargs)

    if reroute_dashbord:
        dashboard_fetcher = "http://cdcihn/transients/dashboard/fetchme"

        print("towards dashboard fetcher",dashboard_fetcher)

        c = requests.get(
                url=dashboard_fetcher, 
                params=dict(url=url+"?"+urllib.parse.urlencode(kwargs))
            )
    else:
        c = requests.get(
                url=url,
                params={**kwargs, '_async_request': True},
                auth=get_auth(),
            )

    try:
        c_j = c.json()
        if c_j.get('workflow_status') != 'done':
            raise WorkflowIncomplete(c_j.get('workflow_status'))
        else:
            output = c_j.get('data').get('output')
    except Exception as ed:
        print("problem decoding:", repr(ed))
        print("raw output:",c.text)
        #logstasher.log(dict(event='failed to decode output',raw_output=c.text, exception=repr(ed)))
        raise


    pngs = []

    for k in output:
        if k.endswith("_content"):
            if k.endswith("_png_content"):
                pngs.append(base64.b64decode(output[k]))
            output[k] = "reduced"
    
    print(json.dumps(output, indent=4, sort_keys=True))

    #for png in pngs:
    #    from PIL import Image
    #    with Image.open(BytesIO(png)) as img:
    #        img.show()

    return output

