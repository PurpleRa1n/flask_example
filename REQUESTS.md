Create product:
curl -d '{
        "name": "Another test product", 
        "description": "Awesome product description.", 
        "price":500, 
        "qty":1
    }'  \
    -H "Content-Type: application/json" \
    -X POST http://127.0.0.1:5000/products/

Get products:
curl -i -H "Accept: application/json" \ 
    -H "Content-Type: application/json" \
    -X GET http://127.0.0.1:5000/products/

Get product:
curl -i -H "Accept: application/json" \ 
    -H "Content-Type: application/json" \
    -X GET http://127.0.0.1:5000/products/1/
    
Update products:
curl -d '{
        "name": "Updated!", 
        "description": "Awesome product description.", 
        "price":1500, 
        "qty":2
    }'  \
    -H "Content-Type: application/json" \
    -X PUT http://127.0.0.1:5000/products/1/
    
Delete products:
curl -X DELETE http://127.0.0.1:5000/products/1/
