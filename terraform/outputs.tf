output "master_external_ip" {
  value = google_compute_instance.master.network_interface[0].access_config[0].nat_ip
}

output "worker1_external_ip" {
  value = google_compute_instance.worker1.network_interface[0].access_config[0].nat_ip
}

output "worker2_external_ip" {
  value = google_compute_instance.worker2.network_interface[0].access_config[0].nat_ip
}

output "master_internal_ip" {
  value = google_compute_instance.master.network_interface[0].network_ip
}

output "worker1_internal_ip" {
  value = google_compute_instance.worker1.network_interface[0].network_ip
}

output "worker2_internal_ip" {
  value = google_compute_instance.worker2.network_interface[0].network_ip
}

output "master_name" {
  value = google_compute_instance.master.name
}

output "worker1_name" {
  value = google_compute_instance.worker1.name
}

output "worker2_name" {
  value = google_compute_instance.worker2.name
}
