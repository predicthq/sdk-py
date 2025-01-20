from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)

# Create a new analysis
# The created analysis id will be returned
analysis = phq.beam.analysis.create(
    name="New Analysis", location__geopoint={"lat": "37.7749", "lon": "-122.4194"}
)
print(analysis.model_dump(exclude_none=True))


# Upload demand data to an analysis
# The demand data can be uploaded from a CSV, NDJSON or JSON file file.abs
# The sdk accepts both a string file path or a file object.abs
# Upload demand data from a CSV file with a string file path
phq.beam.analysis.upload_demand(analysis_id="abc123", csv="./demand.csv")
# Upload demand data from a CSV file with a file object
with open("./demand.csv") as f:
    phq.beam.analysis.upload_demand(analysis_id="abc123", csv=f)

# Upload demand data from a NDJSON file with a string file path
phq.beam.analysis.upload_demand(analysis_id="abc123", ndjson="./demand.ndjson")
# Upload demand data from a NDJSON file with a file object
with open("./demand.ndjson") as f:
    phq.beam.analysis.upload_demand(analysis_id="abc123", ndjson=f)

# Upload demand data from a JSON file with a string file path
phq.beam.analysis.upload_demand(analysis_id="abc123", json="./demand.json")
# Upload demand data from a JSON file with a file object
with open("./demand.json") as f:
    phq.beam.analysis.upload_demand(analysis_id="abc123", json=f)

# Get an analysis
analysis = phq.beam.analysis.get(analysis_id="abc123")
print(analysis.model_dump(exclude_none=True))


# Search for analyses
# The search() method returns an AnalysisResultSet which allows you to iterate
# over the first page of Analysis objects (10 analyses by default)
for analysis in phq.beam.analysis.search(q="My analysis").iter_all():
    print(analysis.model_dump(exclude_none=True))


# Update an analysis
phq.beam.analysis.update(analysis_id="abc123", name="Updated Analysis")


# Delete an analysis
phq.beam.analysis.delete(analysis_id="abc123")


# Refresh an analysis
phq.beam.analysis.refresh(analysis_id="abc123")


# Get correlation results
# The get_correlation_results() method returns a CorrelationResultSet which allows you to iterate
for correlation_result in phq.beam.analysis.get_correlation_results(
    analysis_id="abc123", date__gt="2024-01-01", date__lt="2024-01-31"
).iter_all():
    print(correlation_result.model_dump(exclude_none=True))


# Get feature importance results
feature_importance = phq.beam.analysis.get_feature_importance(analysis_id="abc123")
print(feature_importance.model_dump(exclude_none=True))
