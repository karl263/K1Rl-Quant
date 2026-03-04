---
title: K1RL Quasar
emoji: 🌌
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# K1RL QUASAR — Quantitative Intelligence Observatory

> **HuggingFace Spaces Deployment** | 12GB RAM | Production-Ready AI Training Platform

## 🌌 Overview

K1RL QUASAR is a comprehensive AI training monitoring platform featuring:

- **Real-time Training Metrics** — Actor/Critic loss, AVN accuracy, buffer size
- **Advanced Health Monitoring** — RAM/disk management with auto-cleanup
- **HuggingFace Hub Integration** — Automatic checkpoint management
- **Sleep Prevention** — Keeps HF Spaces active 24/7
- **Multi-Service Architecture** — Redis, Flask, Supervisor orchestration

## 🚀 Services

- **Dashboard** → Port 7860 (HF Spaces standard)
- **Quasar Engine** → Main training loop
- **Health Monitor** → Resource management
- **Redis Server** → Real-time metrics
- **Sleep Prevention** → 24/7 uptime

## 📊 Dashboard Access

- **Main Interface**: `https://KarlQuant-k1rl-quasar.hf.space/`
- **Health Check**: `https://KarlQuant-k1rl-quasar.hf.space/health`
- **Metrics API**: `https://KarlQuant-k1rl-quasar.hf.space/api/metrics`

## ⚙️ Required Secrets

Configure these in Space Settings → Secrets:

```
HF_TOKEN=your_token_here
HF_USERNAME=KarlQuant
REDIS_PASSWORD=k1rl_099a0c008e32300dc3c14189
```

## 🏗️ Architecture

Built with Docker + Supervisor managing multiple services:
- Flask dashboard on port 7860
- Redis for real-time metrics
- Automatic checkpoint backup to HF Hub
- 4-tier RAM monitoring (70% → 78% → 85% → 90%)

---
*K1RL QUASAR — Quantitative Intelligence Observatory*