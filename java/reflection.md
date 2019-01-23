### 注解
java8之前{ present：{ directly preset，inherited }}
自java8 { associated:{ present:{ directly present, inherited }, indirectly present}}

### AnnotatedElement
-   isAnnotationPresent
-   getAnnotation |preset|
-   getAnnotations |preset|
-   getAnnotationsByType |associted|
-   getDeclaredAnnotation |directly present|
-   getDeclaredAnnotationsByType |indirectly present| 
-   getDeclaredAnnotations |directly present|
### GenericDeclaration
泛型声明
-   getTypeParamters
### TypeVariable
-   getBounds
-   getGenericDeclaration
-   getName
-   getAnnotationBounds
### GenericArryType
-   getGenericComponentType
### WildcardType
-   getUpperBounds
-   getLowerBounds
### ParamerterizedType
-   getActualTypeArguments
-   getRawType
-   getOwerType
### AccessibleObject
检查访问权限
