from django.utils.formats import date_format
from django.http import HttpResponse  
from django.conf import settings

from ...core.models import AssignmentGroup, Assignment
from ...ui.defaults import DATETIME_FORMAT

from stream_archives import StreamableZip, StreamableTar


def create_archive_from_assignmentgroups(request, assignmentgroups, file_name, archive_type):
    archive = get_archive_from_archive_type(archive_type)
    it = iter_archive_assignmentgroups(archive, assignmentgroups)
    response = HttpResponse(it, mimetype="application/%s" % archive_type)
    response["Content-Disposition"] = "attachment; filename=%s.%s" % (file_name, archive_type)  
    return response


def create_archive_from_delivery(request, delivery, archive_type):
    archive = get_archive_from_archive_type(archive_type)
    group = delivery.assignment_group
    assignment = group.parentnode
    group_name = get_assignmentgroup_name(group)
    it = iter_archive_deliveries(archive, group_name, assignment.get_path(), [delivery])
    response = HttpResponse(it, mimetype="application/%s" % archive_type)  
    response["Content-Disposition"] = "attachment; filename=%s.%s" % (assignment.get_path(), archive_type)  
    return response


def iter_archive_deliveries(archive, group_name, directory_prefix, deliveries):
    include_delivery_explanation = False
    if len(deliveries) > 1:
        include_delivery_explanation = True
        multiple_deliveries_content = "Delivery-ID    File count    Total size     Delivery time  \r\n"

    for delivery in deliveries:
        metas = delivery.filemetas.all()
        delivery_size = 0
        for f in metas:
            delivery_size += f.size
            filename = "%s/%s/%s" % (directory_prefix, group_name,
                                 f.filename)
            if include_delivery_explanation:
                filename = "%s/%s/%d/%s" % (directory_prefix, group_name,
                                                delivery.number, f.filename)
            # File size is greater than MAX_ARCHIVE_CHUNK_SIZE bytes
            # Write only chunks of size MAX_ARCHIVE_CHUNK_SIZE to the archive
            if f.size > settings.MAX_ARCHIVE_CHUNK_SIZE:
                if not archive.can_write_chunks():
                    raise Exception("The size of file %s is greater than the "\
                                    "maximum allowed size. Download stream aborted.")
                chunk_size = settings.MAX_ARCHIVE_CHUNK_SIZE
                # Open file stream for reading
                file_to_stream = f.read_open()
                # Open a filestream in the archive
                archive.open_filestream(filename, f.size)
                for i in inclusive_range(chunk_size, f.size, chunk_size):
                    bytes = file_to_stream.read(chunk_size)
                    archive.append_file_chunk(bytes, len(bytes))
                    # Read the chunk from the archive and yield the data
                    yield archive.read()
                archive.close_filestream()
            else:
                bytes = f.read_open().read(f.size)
                archive.add_file(filename, bytes)
                # Read the content from the streamable archive and yield the data
                yield archive.read()            
        if include_delivery_explanation:
            multiple_deliveries_content += "  %3d            %3d          %5d        %s\r\n" % \
                                           (delivery.number, len(metas), delivery_size,
                                            date_format(delivery.time_of_delivery, "DATETIME_FORMAT"))
    # Adding file explaining multiple deliveries
    if include_delivery_explanation:
        archive.add_file("%s/%s/%s" %
                         (directory_prefix, group_name,
                          "Deliveries.txt"),
                         multiple_deliveries_content.encode("ascii"))


def iter_archive_assignmentgroups(archive, assignmentgroups):
    """
    Creates an archive, adds files delivered by the assignmentgroups
    and yields the data.
    """
    name_matches = get_dictionary_with_name_matches(assignmentgroups)
    for group in assignmentgroups:
        group_name = get_assignmentgroup_name(group)
        # If multiple groups with the same members exists,
        # postfix the name with assignmentgroup ID.
        if name_matches[group_name] > 1:
            group_name = "%s+%d" % (group_name, group.id)
        deliveries = group.deliveries.all()
        for bytes in iter_archive_deliveries(archive, group_name,
                                             group.parentnode.get_path(),
                                             deliveries):
            yield bytes
    archive.close()
    yield archive.read()


def get_archive_from_archive_type(archive_type):
    archive = None
    if archive_type == 'zip':
        archive = StreamableZip()
    elif archive_type == 'tar' or archive_type == 'tgz' or archive_type == 'tar.gz':
        archive = StreamableTar(archive_type)
    else:
        raise Exception("archive_type is invalid:%s" % archive_type)
    return archive


def verify_groups_not_exceeding_max_file_size(groups):
    for g in groups:
        verify_deliveries_not_exceeding_max_file_size(g.deliveries.all())

def verify_deliveries_not_exceeding_max_file_size(deliveries):
    max_size = settings.MAX_ARCHIVE_CHUNK_SIZE
    for d in deliveries:
        for f_meta in d.filemetas.all():
            if f_meta.size > max_size:
                raise Exception()

def inclusive_range(start, stop, step=1):
    """
    A range() clone, but this includes the right limit
    as is if the last step doesn't divide on stop
    """
    l = []
    x = start
    while x <= stop:
        l.append(x)
        x += step
    if x > stop:
        l.append(stop)
    return l

def get_assignmentgroup_name(assigmentgroup):
    """
    Returns a string containing the group member of the
    assignmentgroup separated by '-'.
    """
    cands = assigmentgroup.get_candidates()
    cands = cands.replace(", ", "-")
    return cands

def get_dictionary_with_name_matches(assignmentgroups):
    """
    Takes a list of assignmentgroups and returns
    a dictionary containing the count of groups
    with similar names sa values in the dictionary.
    """
    matches = {}
    for assigmentgroup in assignmentgroups:
        name = get_assignmentgroup_name(assigmentgroup)
        if matches.has_key(name):
            matches[name] =  matches[name] + 1
        else:
            matches[name] = 1
    return matches
