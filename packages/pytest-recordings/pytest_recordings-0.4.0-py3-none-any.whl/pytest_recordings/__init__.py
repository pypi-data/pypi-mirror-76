import os

record_dir = "C:/tmp/test-results/records"
setup_record_dir = f"{record_dir}/pre-test-setup"

if not os.path.exists(record_dir):
    os.makedirs(record_dir)

if not os.path.exists(setup_record_dir):
    os.makedirs(setup_record_dir)
