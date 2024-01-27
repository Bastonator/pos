#remove the """""""" at the top and bottom to see better
"""
data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        #.filter(branch_owner_id=pk) was added as example of howw the filter fuction might look when tehre are multile barnches
        category = Category.objects.filter(id = data['category_id']).filter(branch_owner_id=pk).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


data =  request.POST
resp = {'status':'failed'}
try:
    if (data['id']).isnumeric() and int(data['id']) > 0 :
        save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
    else:
        save_category = Category(name=data['name'], description = data['description'],status = data['status'])
        save_category.save()
    resp['status'] = 'success'
    messages.success(request, 'Category Successfully saved.')
except:
    resp['status'] = 'failed'
return HttpResponse(json.dumps(resp), content_type="application/json")   
"""