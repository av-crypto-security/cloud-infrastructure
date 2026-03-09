install-client:
	sudo apt update
	sudo apt install -y clickhouse-client

connect:
	clickhouse-client \
	--host $(HOST) \
	--secure \
	--user $(USER) \
	--database $(DB) \
	--port 9440 \
	--ask-password

create-table:
	clickhouse-client \
	--host $(HOST) \
	--secure \
	--user $(USER) \
	--database $(DB) \
	--port 9440 \
	-q "CREATE TABLE IF NOT EXISTS metrics \
	(timestamp DateTime, \
	service String, \
	region String, \
	cpu_usage Float32, \
	memory_usage Float32, \
	request_latency_ms UInt32, \
	error_rate Float32) \
	ENGINE = MergeTree ORDER BY timestamp" \
	--ask-password

ingest:
	cat example-metrics.tsv | clickhouse-client \
	--host $(HOST) \
	--secure \
	--user $(USER) \
	--database $(DB) \
	--port 9440 \
	-q "INSERT INTO metrics FORMAT TabSeparated" \
	--ask-password
