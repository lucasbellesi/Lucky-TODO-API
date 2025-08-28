def test_categories_crud_minimal(test_client):
    # Create category
    r = test_client.post("/categories/", json={"name": "Work", "color": "#ff0000"})
    assert r.status_code in (200, 201), r.text
    cat = r.json()
    assert cat["name"] == "Work"
    assert cat["color"] == "#ff0000"

    # List categories
    r = test_client.get("/categories/")
    assert r.status_code == 200
    cats = r.json()
    assert any(c["id"] == cat["id"] for c in cats)

