from fastapi import APIRouter, Depends
from pydantic import BaseModel
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.security import verify_api_key

router = APIRouter(prefix="/router", tags=["RBF Router"], dependencies=[Depends(verify_api_key)])

class QueryRequest(BaseModel):
    query: str

class RBFRouter:
    def __init__(self):
        self.scaler = StandardScaler()
        self.centers = None
        self.weights = None
        self.is_trained = False
        self.gamma = 0.05
        self.tiers = ["small", "medium", "frontier"]

    def _extract_features(self, query):
        words = query.split()
        return np.array([
            len(query), len(words), len(query)/max(len(words),1),
            sum(c.isdigit() for c in query), query.count("?"),
            sum(1 for kw in ["design", "architecture", "proof"] if kw in query.lower())
        ], dtype=np.float64)

    def fit(self):
        # Bootstrap with synthetic data
        X = np.array([
            [10, 2, 5, 0, 1, 0], [20, 4, 5, 0, 1, 0], # Small
            [50, 10, 5, 0, 1, 0], [60, 12, 5, 0, 1, 0], # Medium
            [100, 20, 5, 0, 1, 1], [120, 25, 5, 0, 1, 1] # Frontier
        ])
        y = np.array([0, 0, 1, 1, 2, 2])
        X_scaled = self.scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_scaled)
        self.centers = kmeans.cluster_centers_
        
        H = np.exp(-self.gamma * np.linalg.norm(X_scaled[:, None] - self.centers, axis=2)**2)
        Y = np.zeros((len(y), 3))
        Y[np.arange(len(y)), y] = 1
        self.weights = np.linalg.pinv(H) @ Y
        self.is_trained = True

    def predict(self, query):
        if not self.is_trained: self.fit()
        feat = self._extract_features(query).reshape(1, -1)
        X_scaled = self.scaler.transform(feat)
        H = np.exp(-self.gamma * np.linalg.norm(X_scaled[:, None] - self.centers, axis=2)**2)
        probs = H @ self.weights
        probs = np.exp(probs - np.max(probs)) / np.sum(np.exp(probs - np.max(probs)))
        return self.tiers[np.argmax(probs[0])], float(np.max(probs[0]))

rbf_model = RBFRouter()

@router.post("/predict")
def predict_tier(req: QueryRequest):
    tier, confidence = rbf_model.predict(req.query)
    return {"query": req.query, "tier": tier, "confidence": round(confidence, 3)}