APP_ID=hosted-canvas2d
APP_HOST=${APP_ID}.appspot.com
APP_NS=hosted.canvas2d.org

# uploading to localhost:
#   make restore(-accounts) APP_ID=dev~hosted-canvas2d \
#                			APP_HOST=localhost:8080 \
#                			APP_NS=localhost

# uploading to hosted.umlcanvas.org
#   make restore(-accounts) APP_NS=hosted.umlcanvas.org

APPCFG=appcfg.py
APPCFG_APP=--application=${APP_ID} \
           --url=http://${APP_HOST}/_ah/remote_api

KINDS=Diagram DiagramVersion
BACKUP_DIR=backup

APPCFG_CREATE=${APPCFG} create_bulkloader_config ${APPCFG_APP} \
			   			--filename=bulkloader.yaml
APPCFG_DOWNLOAD=${APPCFG} download_data ${APPCFG_APP} \
						  --config_file=bulkloader.yaml
APPCFG_UPLOAD=${APPCFG} upload_data ${APPCFG_APP} \
						--config_file=bulkloader.yaml

all:

prepare:
	@echo "*** building legacy entities for restore"
	@./prepare.pl < diagrams.tsv
	@iconv -f ISO-8859-1 -t UTF-8 Diagram.csv > Diagram-utf8.csv
	@mv Diagram-utf8.csv Diagram.csv
	@iconv -f ISO-8859-1 -t UTF-8 DiagramVersion.csv > DiagramVersion-utf8.csv
	@mv DiagramVersion-utf8.csv DiagramVersion.csv

backup: clean bulkloader.yaml
	@for kind in ${KINDS}; do \
		echo "*** backing up ${APP_NS} $${kind}s"; \
		${APPCFG_DOWNLOAD} --namespace=${APP_NS} \
						   --filename=$${kind}.csv \
						   --kind=$${kind}; \
	done

backup-accounts:
	@echo "*** backing up global Accounts"
	@${APPCFG_DOWNLOAD} --namespace=-global- \
					    --filename=Account.csv \
					    --kind=Account
bulkloader.yaml:
	@echo "*** creating bulkloader configuration"
	${APPCFG_CREATE}
	@echo "Edit the bulkloader.yaml configuration file before you continue."
	@echo "press any key to continue..."
	@read

restore:
	@for kind in ${KINDS}; do \
		echo "*** restoring ${APP_NS} $${kind}s"; \
		${APPCFG_UPLOAD} --namespace=${APP_NS} \
						 --filename=$${kind}.csv \
						 --kind=$${kind}; \
	done

restore-accounts:
	@echo "*** restoring global Accounts"
	@${APPCFG_UPLOAD} --namespace=-global- \
					  --filename=Account.csv \
					  --kind=Account

clean:
	@rm -f *.csv
	@rm -rf bulkloader-{log,progress,results}*	
