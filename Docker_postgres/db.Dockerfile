FROM postgres:14.2-alpine

ENV POSTGRES_DB ecommerce_db
ENV POSTGRES_USER mohammadhssn
ENV POSTGRES_PASSWORD mohammadhssn

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/