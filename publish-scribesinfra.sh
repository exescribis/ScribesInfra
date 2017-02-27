#!/usr/bin/env bash
git -C ~/DEV/ScribesZone/ScribesInfra/ add .
git -C ../../ScribesZone/ScribesInfra/ commit -m 'bulk update'
git -C ../../ScribesZone/ScribesInfra/ push origin master