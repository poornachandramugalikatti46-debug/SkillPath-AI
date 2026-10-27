import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("data/student_training_data.csv")

print("Dataset loaded!")
print("Shape:", df.shape)


# ==========================================
# 2. Select features
# ==========================================

features = [
    "cgpa",

    "python_score",
    "java_score",
    "sql_score",
    "dsa_score",
    "frontend_score",
    "backend_score",
    "ml_score",
    "cloud_score",

    "resume_skill_count",
    "project_count",
    "internship_count",
    "certification_count",
    "experience_months",

    "github_repo_count",
    "github_language_count",
    "github_star_count",
    "github_fork_count",
    "github_project_count",
    "github_activity_score",

    "technical_score",
    "aptitude_score",
    "problem_solving_score",
    "communication_score",
    "interview_confidence_score"
]

X = df[features]


# ==========================================
# 3. Standardize features
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nFeatures standardized!")


# ==========================================
# 4. Find good number of clusters
# ==========================================

print("\nTesting different cluster counts...")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels
    )

    print(
        f"K = {k} | "
        f"Silhouette Score = {score:.4f}"
    )


# ==========================================
# 5. Train final K-Means
# ==========================================

NUMBER_OF_CLUSTERS = 4

kmeans = KMeans(
    n_clusters=NUMBER_OF_CLUSTERS,
    random_state=42,
    n_init=10
)

cluster_labels = kmeans.fit_predict(X_scaled)

df["cluster"] = cluster_labels


print("\nK-Means clustering completed!")


# ==========================================
# 6. Cluster distribution
# ==========================================

print("\nCluster distribution:")

print(
    df["cluster"].value_counts().sort_index()
)


# ==========================================
# 7. PCA for visualization
# ==========================================

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

df["pca_1"] = X_pca[:, 0]
df["pca_2"] = X_pca[:, 1]


print("\nPCA completed!")

print(
    "Explained variance:",
    pca.explained_variance_ratio_
)


# ==========================================
# 8. Analyze clusters
# ==========================================

cluster_summary = df.groupby("cluster")[
    [
        "cgpa",
        "python_score",
        "sql_score",
        "dsa_score",
        "project_count",
        "internship_count",
        "github_repo_count",
        "github_activity_score",
        "technical_score",
        "problem_solving_score",
        "communication_score"
    ]
].mean()


print("\n==========================================")
print("CLUSTER SUMMARY")
print("==========================================")

print(
    cluster_summary.round(2)
)


# ==========================================
# 9. Save clustering models
# ==========================================

joblib.dump(
    scaler,
    "models/clustering_scaler.joblib"
)

joblib.dump(
    kmeans,
    "models/student_kmeans.joblib"
)

joblib.dump(
    pca,
    "models/student_pca.joblib"
)


print("\nClustering models saved!")


# ==========================================
# 10. Save cluster data
# ==========================================

df.to_csv(
    "data/student_training_with_clusters.csv",
    index=False
)

print(
    "\nClustered dataset saved to:"
    " data/student_training_with_clusters.csv"
)