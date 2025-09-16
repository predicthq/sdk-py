from predicthq import Client

# Please copy paste your access token here
# or read our Quickstart documentation if you don't have a token yet
# https://docs.predicthq.com/guides/quickstart/
ACCESS_TOKEN = "abc123"

phq = Client(access_token=ACCESS_TOKEN)

# Create a new analysis group
# The created group id will be returned
group = phq.beam.analysis_group.create(name="New Analysis Group", analysis_ids=["abc123", "def456"])
print(group.model_dump(exclude_none=True))


# Get an analysis group
group = phq.beam.analysis_group.get(group_id="abc123")
print(group.model_dump(exclude_none=True))


# Search for analysis groups
# The search() method returns an AnalysisGroupResultSet which allows you to iterate
# over the first page of AnalysisGroup objects (10 groups by default)
for group in phq.beam.analysis_group.search(q="My analyis group").iter_all():
    print(group.model_dump(exclude_none=True))


# Update an analysis group
phq.beam.analysis_group.update(group_id="abc123", name="Updated Analysis Group")


# Delete an analysis group
phq.beam.analysis_group.delete(group_id="abc123")


# Refresh an analysis group
phq.beam.analysis_group.refresh(group_id="abc123")


# Get feature importance results
group_feature_importance = phq.beam.analysis_group.get_feature_importance(group_id="abc123")
print(group_feature_importance.model_dump(exclude_none=True))
