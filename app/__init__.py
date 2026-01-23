from fastapi import FastAPI

app = FastAPI(
  title="HotBed.lk API Interface",
  description="API for HotBed.lk, a platform for booking accommodations in Sri Lanka.",
  version="1.0.0",
  contact={
    "name": "HotBed.lk Support",
    "url": "https://hotbed.lk/contact",
    "email": "mail@hotbed.lk"
  }
)
