SELECT "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."price",
       "shopapp_product"."discount",
       "sh
      opapp_product"."created_at",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
FROM "shopapp_product"
WHERE "shopapp_product"."id" = 13 LIMIT 21;

SELECT "shopapp_productimage"."id",
       "shopapp_productimage"."product_id",
       "shopapp_productimage"."image",
       "shopapp_productimage"."description"
FROM "shopapp_productimage"
WHERE "shopapp_productimage"."product_id" IN (13);




SELECT "blogapp_article"."id"
     , "blogapp_article"."title"
     , "blogapp_article"."pub_date"
     , "blogapp_article"."author_id"
     , "blogapp_article"."category_id"
     , "blogapp_author"."id"
     , "blogapp_author"."name"
     , "blogapp_author"."bio"
     , "blogapp_category"."id"
     , "blogapp_category"."name"
FROM "blogapp_article"
         INNER JOIN
     "blogapp_author" ON ("blogapp_article"."author_id" = "blogapp_author"."id")
         INNER JOIN "blogapp_category" ON ("blogapp_article"."category_id" = "blogapp_category"."id");
args
=(); alias
=default
SELECT ("blogapp_article_tags"."article_id") AS "_prefetch_related_val_article_id",
       "blogapp_tag"."id",
       "blogapp_tag"."name"
FROM "blogapp_tag"
         INNER JOIN "blogapp_article_tags" ON ("blogapp_tag"."id" = "blogapp_article_tags"."tag_id")
WHERE "blogapp_article_tags"."article_id" IN (1);
args
=(1,); alias
=default

