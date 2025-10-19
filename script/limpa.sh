# web-101: manter só 2
for t in $(curl -s http://localhost:5000/v2/web-101/tags/list | jq -r '.tags[]'); do
  [ "$t" = "2" ] && continue
  d=$(curl -sI -H 'Accept: application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json' \
      http://localhost:5000/v2/web-101/manifests/$t | awk -F': ' '/Docker-Content-Digest/ {print $2}' | tr -d $'\r')
  curl -s -X DELETE http://localhost:5000/v2/web-101/manifests/$d >/dev/null
done

# web-102: manter só 2
for t in $(curl -s http://localhost:5000/v2/web-102/tags/list | jq -r '.tags[]'); do
  [ "$t" = "2" ] && continue
  d=$(curl -sI -H 'Accept: application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json' \
      http://localhost:5000/v2/web-102/manifests/$t | awk -F': ' '/Docker-Content-Digest/ {print $2}' | tr -d $'\r')
  curl -s -X DELETE http://localhost:5000/v2/web-102/manifests/$d >/dev/null
done

# GC final
docker compose exec registry registry garbage-collect --delete-untagged /etc/docker/registry/config.yml

