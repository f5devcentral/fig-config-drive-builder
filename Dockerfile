ARG base_container=f5devcentral/f5-icontrol-gateway

FROM "${base_container}"

ENV app_name=fig-config-drive-builder
RUN mkdir -p "/var/lib/${app_name}"
COPY / "/var/lib/${app_name}/"
RUN chown -R nginx:nginx "/var/lib/${app_name}"

COPY unit_config.conf "/etc/unit/${app_name}.conf"
