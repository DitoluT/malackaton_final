# malackaton_final
# Proyecto de Gestión de Embalses en Oracle Cloud

## Introducción

Como participante en este proyecto, tendrás la oportunidad de trabajar con datos sobre embalses españoles utilizando la infraestructura de Oracle Cloud (OCI). El objetivo es desarrollar una aplicación que gestione y analice información de embalses, permitiendo el acceso a datos relevantes de manera segura y eficiente.

## Estructura de Datos

Para comenzar, debes familiarizarte con las tablas de datos que utilizarás. Hay tres tablas principales que contienen información sobre los embalses:

### Tabla: EMBALSES

Esta tabla incluye los siguientes campos:

- **ID**: Identificador único del embalse.
- **AMBITO_NOMBRE**: Nombre del ámbito del embalse.
- **EMBALSE_NOMBRE**: Nombre específico del embalse.
- **AGUA_TOTAL**: Cantidad total de agua que puede almacenar el embalse.
- **ELECTRICO_FLAG**: Un indicador que señala si el embalse se utiliza para generar electricidad.

### Tabla: AGUA_ALMACENADA

Esta tabla proporciona datos sobre la cantidad de agua almacenada:

- **FECHA**: Fecha de registro de la información.
- **AGUA_ACTUAL**: Cantidad actual de agua en el embalse en esa fecha.
- **ID**: Identificador del embalse, que relaciona esta tabla con la tabla EMBALSES.

### Tabla Complementaria: LISTADO_EMBALSES

Esta tabla contiene información adicional sobre los embalses y sus características:

- **CODIGO**: Código del embalse.
- **NOMBRE**: Nombre del embalse.
- **EMBALSE**: Información adicional sobre el embalse.
- **X/Y**: Coordenadas geográficas.
- **DEMARC**: Demarcación hidrográfica.
- **CAUCE**: Cauce del embalse.
- **GOOGLE, OPENSTREETMAP, WIKIDATA**: Enlaces a recursos externos.
- **PROVINCIA, CCAA**: Localización del embalse.
- **TIPO, TITULAR, USO**: Información sobre el tipo de embalse, su titularidad y uso.
- **COTA_CORON, ALT_CIMIEN**: Datos sobre la altura y características estructurales.
- **INFORME**: Información adicional sobre el embalse.

Ten en cuenta que no existe una correspondencia perfecta entre los datos de las tablas EMBALSES y LISTADO_EMBALSES, lo que añade un reto adicional a tu proyecto.

## Fases del Proyecto

### Fase 1 (Obligatoria)

1. **Descarga de Datos**: Descarga la información de las tres tablas mencionadas desde la página de estudiantes del CV y cárgala en un usuario de la base

