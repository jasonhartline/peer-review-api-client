import csv
import sys
from api_client import client


def submit_request(reviewer_pool_id, submission_pool_id):
    config = None
    # Setting config=None is equivalent to the following default configuration:
    # config = {
    #     "ignorePapersPublishedBefore": 2011, # current year - 10
    #     "ignorePapersPublishedAfter": None,  # No restriction
    #     "maximumPapersPerReviewer": 100,     # Consider only the 100 most recent papers by each reviewer
    #     "nearestPaperCount": 3,              # Compute score based on 3 paper most similar to the submission
    #     "similarityMeasure": "COSINE",       # Use cosine similarity
    #     "weighting": "INVERSE_RANK"          # Use weighted average of similarity scores
    # }
    req = {'reviewerPoolId': reviewer_pool_id, 'submissionPoolId': submission_pool_id,
           'configuration': config}
    return client().post('reviewer-match', req)['id']


def list_requests():
    return client().get('reviewer-match')

def print_requests():
    requests = list_requests()
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['id', 'status', 'reviewerPoolId', 'submissionPoolId',
                                        'configuration', 'submitted'])
    writer.writeheader()
    for r in requests:
        writer.writerow(r)

def download_result(request_id):
    return client().get(f'reviewer-match/{request_id}/result')

def print_result(request_id):
    results = download_result(request_id)
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=['reviewerId', 'reviewerExternalId', 'submissionId', 'submissionExternalId', 'score', 'reason'])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

