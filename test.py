#!/usr/bin/env python3
import boto3, json, sys

def main():
    region     = boto3.Session().region_name
    bucket     = f"jumpstart-cache-prod-{region}"
    manifest   = "models_manifest.json"
    MODEL_ID   = "tensorflow-tc-bert-en-uncased-L-12-H-768-A-12-2"

    s3 = boto3.client("s3", region_name=region)
    # 1. Download the full manifest
    s3.download_file(bucket, manifest, manifest)

    # 2. Find our model entry
    with open(manifest) as f:
        all_models = json.load(f)

    entry = next((m for m in all_models if m["model_id"] == MODEL_ID), None)
    if not entry:
        print(f"❌ Couldn’t find model {MODEL_ID} in manifest", file=sys.stderr)
        sys.exit(1)

    # 3. Download the per‐model spec JSON
    spec_key = entry["spec_key"]
    s3.download_file(bucket, spec_key, "model_spec.json")
    with open("model_spec.json") as f:
        spec = json.load(f)

    # 4. Build the S3 model URL
    #    spec["hosting_artifact_key"] is something like "blazingtext-text-classification/model.tar.gz"
    artifact_key    = spec["hosting_artifact_key"]
    model_data_url  = f"s3://{bucket}/{artifact_key}"

    # 5. Build the ECR image URI
    #    spec["hosting_ecr_specs"] has framework/version info
    ecr            = spec["hosting_ecr_specs"]
    framework      = ecr["framework"]           # e.g. "tensorflow"
    fw_ver         = ecr["framework_version"]   # e.g. "2.8"
    # JumpStart inference images live in AWS account 763104351884
    # and the image is named "<framework>-inference:<version>-gpu"
    container_image_uri = (
        f"763104351884.dkr.ecr.{region}.amazonaws.com/"
        f"{framework}-inference:{fw_ver}-gpu"
    )

    # 6. Print out the two lines you can paste into your shell
    print(f'export PRETRAINED_CONTAINER_URI="{container_image_uri}"')
    print(f'export PRETRAINED_MODEL_S3_URL="{model_data_url}"')

if __name__ == "__main__":
    main()

