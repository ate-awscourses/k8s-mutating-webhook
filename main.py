from fastapi import FastAPI, Request
import base64
import json

app = FastAPI()

@app.post("/mutate")
async def mutate_request(request: Request):
    # 1. Parse the incoming Kubernetes AdmissionReview payload
    payload = await request.json()
    req = payload.get("request", {})
    uid = req.get("uid", "")
    
    # 2. Extract the object being deployed (e.g., a Pod)
    k8s_object = req.get("object", {})
    metadata = k8s_object.get("metadata", {})
    labels = metadata.get("labels", {})
    
    patch_operations = []
    
    # 3. Check for the label and define the modification
    if "env" not in labels:
        # If the labels dictionary is completely empty, initialize it
        if not labels:
            patch_operations.append({
                "op": "add",
                "path": "/metadata/labels",
                "value": {"env": "production"}
            })
        # Otherwise, just append the new label to the existing dictionary
        else:
            patch_operations.append({
                "op": "add", 
                "path": "/metadata/labels/env", 
                "value": "production"
            })
            
    # 4. Kubernetes requires the JSON patch array to be Base64 encoded
    patch_json_string = json.dumps(patch_operations)
    patch_base64 = base64.b64encode(patch_json_string.encode("utf-8")).decode("utf-8")
    
    # 5. Return the AdmissionResponse back to the Kubernetes API server
    return {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": True,           
            "patchType": "JSONPatch",  
            "patch": patch_base64      
        }
    }
